import sqlite3
import psycopg

# Connect to SQLite and read all records.
sqlite_conn = sqlite3.connect("history.db")
sqlite_conn.row_factory = sqlite3.Row

rows = sqlite_conn.execute("""
    SELECT id, prompt, steps, seed, image_path, created_at
    FROM generations
    ORDER BY id
""").fetchall()

print(f"Found {len(rows)} SQLite records")

# Copy records to PostgreSQL.
with psycopg.connect("dbname=local_ai_studio") as pg_conn:
    with pg_conn.cursor() as cursor:
        for row in rows:
            cursor.execute("""
                INSERT INTO generations
                    (id, prompt, steps, seed, image_path, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, tuple(row))

        # Adjust the automatic ID sequence.
        cursor.execute("""
            SELECT setval(
                pg_get_serial_sequence('generations', 'id'),
                COALESCE(MAX(id), 1),
                MAX(id) IS NOT NULL
            )
            FROM generations
        """)

sqlite_conn.close()

print("Migration completed successfully")