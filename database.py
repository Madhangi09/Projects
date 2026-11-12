
import sqlite3

DB_NAME = "mindmaze.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_score(name, difficulty, score):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO players (name, difficulty, score) VALUES (?, ?, ?)",
        (name, difficulty, score)
    )

    conn.commit()
    conn.close()


def get_leaderboard():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, difficulty, score
        FROM players
        ORDER BY score DESC
        LIMIT 10
    """)

    results = cursor.fetchall()
    conn.close()

    return results
