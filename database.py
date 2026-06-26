
import sqlite3

DATABASE = "nexora.db"

def connect():
    return sqlite3.connect(DATABASE)

def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT UNIQUE,
        full_name TEXT,
        referral_code TEXT UNIQUE,
        referred_by TEXT,
        balance REAL DEFAULT 0,
        points INTEGER DEFAULT 0,
        is_admin INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")
