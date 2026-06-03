import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    api_key TEXT PRIMARY KEY,
                    refresh_token TEXT,
                    email TEXT
                 )''')
    conn.commit()
    conn.close()

def save_user_auth(api_key: str, refresh_token: str, email: str = ""):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (api_key, refresh_token, email) VALUES (?, ?, ?)", 
              (api_key, refresh_token, email))
    conn.commit()
    conn.close()

def get_refresh_token(api_key: str):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT refresh_token FROM users WHERE api_key = ?", (api_key,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None
    except Exception:
        return None

def get_email_by_api_key(api_key: str):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT email FROM users WHERE api_key = ?", (api_key,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None
    except Exception:
        return None
