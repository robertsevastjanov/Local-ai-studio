import sqlite3
import sys
from pathlib import Path

# Receive the image path from the command line.
image_path = sys.argv[1]
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "history.db"

# Connect to the SQLite database.
with sqlite3.connect(DB_PATH) as connection:
    row = connection.execute(
        """
        SELECT id, prompt, steps, seed, image_path
        FROM generations
        WHERE image_path = ?
        """,
        (image_path,)
    ).fetchone()

# Return a result to the calling process.
if row is None:
    print("Generation not found")
    sys.exit(1)

# Receive expected values from Playwright.
expected_prompt = sys.argv[2]
expected_steps = int(sys.argv[3])
expected_seed = int(sys.argv[4])

# Compare actual SQLite values with expected values.
assert row[1] == expected_prompt, "Prompt mismatch"
assert row[2] == expected_steps, "Steps mismatch"
assert row[3] == expected_seed, "Seed mismatch"
print("Generation found:", row)
sys.exit(0)