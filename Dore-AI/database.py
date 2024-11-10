# database.py
import sqlite3
from datetime import datetime

DB_NAME = 'chat_history.db'
ERROR_LOG_FILE = 'error_log.txt'

def log_error(error_message):
    with open(ERROR_LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] ERROR: {error_message}\n")

def connect_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                message TEXT,
                is_user INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        return conn
    except sqlite3.Error as e:
        log_error(f"Database connection error: {e}")
        return None

def save_message(user_name, message, is_user):
    try:
        conn = connect_db()
        if conn:
            conn.execute(
                "INSERT INTO chat_history (user_name, message, is_user) VALUES (?, ?, ?)",
                (user_name, message, is_user)
            )
            conn.commit()
            conn.close()
    except sqlite3.Error as e:
        log_error(f"Error saving message: {e}")

def get_chat_history(user_name):
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT message, is_user, timestamp FROM chat_history WHERE user_name = ?",
                (user_name,)
            )
            history = cursor.fetchall()
            conn.close()
            return history
    except sqlite3.Error as e:
        log_error(f"Error retrieving chat history: {e}")
        return []

def delete_chat_history(user_name):
    try:
        conn = connect_db()
        if conn:
            conn.execute("DELETE FROM chat_history WHERE user_name = ?", (user_name,))
            conn.commit()
            conn.close()
    except sqlite3.Error as e:
        log_error(f"Error deleting chat history: {e}")
