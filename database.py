import os
import sqlite3
import psycopg

DB_PATH = "history.db"
POSTGRES_DSN = os.getenv("DATABASE_URL", "dbname=local_ai_studio")


def connect_postgres():
    return psycopg.connect(POSTGRES_DSN)

def save_postgres_generation(prompt, steps, seed, image_path):
    with connect_postgres() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO generations (prompt, steps, seed, image_path)
                VALUES (%s, %s, %s, %s)
                RETURNING id, created_at
            """, (prompt, steps, seed, image_path))

            generation_id, created_at = cursor.fetchone()

    return generation_id, created_at.strftime("%Y-%m-%d %H:%M:%S")

def get_postgres_generations():
    with connect_postgres() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, prompt, steps, seed, image_path, created_at
                FROM generations
                ORDER BY id DESC
                LIMIT 500
            """)

            columns = [column.name for column in cursor.description]
            rows = cursor.fetchall()

    return [
        {
            **dict(zip(columns, row)),
            "created_at": row[-1].strftime("%Y-%m-%d %H:%M:%S")
        }
        for row in rows
    ]

def init_db():
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            steps INTEGER NOT NULL,
            seed INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    connection.close()

def save_generation(prompt, steps, seed, image_path):
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        INSERT INTO generations (prompt, steps, seed, image_path)
        VALUES (?, ?, ?, ?)
    """, (prompt, steps, seed, image_path))

    connection.commit()
    connection.close()

def save_sqlite_backup(generation_id, prompt, steps, seed, image_path, created_at):
    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("""
            INSERT INTO generations
                (id, prompt, steps, seed, image_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                prompt = excluded.prompt,
                steps = excluded.steps,
                seed = excluded.seed,
                image_path = excluded.image_path,
                created_at = excluded.created_at
        """, (
            generation_id,
            prompt,
            steps,
            seed,
            image_path,
            created_at
        ))

        connection.commit()
    finally:
        connection.close()

def save_generation_with_backup(prompt, steps, seed, image_path):
    # 1. Save to the primary PostgreSQL database.
    generation_id, created_at = save_postgres_generation(
        prompt, steps, seed, image_path
    )

    # 2. Save the same record to backup SQLite.
    save_sqlite_backup(
        generation_id,
        prompt,
        steps,
        seed,
        image_path,
        created_at
    )

    return generation_id

def get_generations():
    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    cursor = connection.execute("""
        SELECT id, prompt, steps, seed, image_path, created_at
        FROM generations
        ORDER BY id DESC
        LIMIT 500
    """)

    generations = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return generations

if __name__ == "__main__":
    init_db()