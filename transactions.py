import sqlite3
from datetime import date

def add_transaction(user_id, t_type, category, amount, description=""):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO transactions 
        (user_id, type, category, amount, date, description)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, t_type, category, amount, date.today(), description)
    )
    conn.commit()
    conn.close()
    print("✅ Transaction added")

def delete_transaction(transaction_id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
    conn.commit()
    conn.close()
