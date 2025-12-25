import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        print("✅ Registration successful")
        conn.close()
        return True
    except sqlite3.IntegrityError:
        print("❌ Username already exists")
        conn.close()
        return False

def login_user(username, password):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None
