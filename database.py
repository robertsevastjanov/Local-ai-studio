import sqlite3

DB_PATH = "history.db"


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

def get_generations():
    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    cursor = connection.execute("""
        SELECT id, prompt, steps, seed, image_path, created_at
        FROM generations
        ORDER BY id DESC
        LIMIT 50
    """)

    generations = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return generations

if __name__ == "__main__":
    init_db()