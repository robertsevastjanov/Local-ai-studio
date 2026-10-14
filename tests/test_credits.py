import pytest
import psycopg
from concurrent.futures import ThreadPoolExecutor

from database import deduct_credits, save_generation_with_credits


def test_rejects_negative_credit_amount():
    with pytest.raises(ValueError):
        deduct_credits(1, -7)

def test_rejects_zero_credit_amount():
    with pytest.raises(ValueError):
        deduct_credits(1, 0)

def test_successful_credit_deduction(test_account):
    new_balance = deduct_credits(test_account, 7)

    assert new_balance == 93

@pytest.mark.parametrize("test_account", [20], indirect=True)

def test_insufficient_credits(test_account):
    from database import connect_postgres
    result = deduct_credits(test_account, 100)

    assert result is None
    with connect_postgres() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT balance FROM credit_accounts WHERE id = %s",
                (test_account,)
            )
            balance_after = cursor.fetchone()[0]

    assert balance_after == 20

@pytest.fixture
def test_account(request):
    from database import connect_postgres
    initial_balance = getattr(request, "param", 100)

    with connect_postgres() as connection:
        if connection.info.dbname != "local_ai_studio_test":
            pytest.fail("Test requires local_ai_studio_test database")

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO credit_accounts (balance) VALUES (%s) RETURNING id",
                (initial_balance,)
            )
            account_id = cursor.fetchone()[0]

    try:
        yield account_id

    finally:
        with connect_postgres() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM credit_accounts WHERE id = %s",
                    (account_id,)
                )

def test_rejects_nonexistent_account():
    result = deduct_credits(-1, 10)

    assert result is None

def test_deducts_entire_balance(test_account):
    new_balance = deduct_credits(test_account, 100)

    assert new_balance == 0

def test_cannot_deduct_twice_from_empty_account(test_account):
    first_result = deduct_credits(test_account, 100)
    second_result = deduct_credits(test_account, 100)

    assert first_result == 0
    assert second_result is None

def test_concurrent_credit_deductions(test_account):
    def spend_credits():
        return deduct_credits(test_account, 80)
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: spend_credits(), range(2)))
    assert sorted(results, key=lambda x: x is None) == [20, None]

def test_generation_with_credits(test_account):
    from database import connect_postgres

    generation_id = None

    try:
        result = save_generation_with_credits(
            account_id=test_account,
            amount=10,
            prompt="A futuristic city at night",
            steps=8,
            seed=42,
            image_path="images/test_transaction.png"
        )

        generation_id = result["generation_id"]

        assert result["remaining_credits"] == 90
        assert isinstance(result["generation_id"], int)
    
    finally:
        if generation_id is not None:
            with connect_postgres() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM generations WHERE id = %s",
                        (generation_id,)
                    )

def test_generation_failure_rolls_back_credits(test_account):
    from database import connect_postgres

    with pytest.raises(psycopg.errors.NotNullViolation):
        save_generation_with_credits(
            account_id=test_account,
            amount=10,
            prompt=None,
            steps=8,
            seed=42,
            image_path="images/test_rollback.png"
        )

    with connect_postgres() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT balance FROM credit_accounts WHERE id = %s",
                (test_account,)
            )
            balance = cursor.fetchone()[0]

    assert balance == 100