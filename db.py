import sqlite3

def get_connection():
    return sqlite3.connect("database.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS websites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        status TEXT,
        last_checked TEXT
    )
    """)

    conn.commit()
    conn.close()