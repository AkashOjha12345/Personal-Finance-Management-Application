import sqlite3
from datetime import date, datetime

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

def delete_transaction(transaction_id, user_id=None):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    if user_id:
        cursor.execute("DELETE FROM transactions WHERE id=? AND user_id=?", (transaction_id, user_id))
    else:
        cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
    conn.commit()
    conn.close()

def get_user_transactions(user_id, limit=10):
    """Get recent transactions for a user"""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, type, category, amount, date, description
        FROM transactions
        WHERE user_id=?
        ORDER BY date DESC, id DESC
        LIMIT ?
    """, (user_id, limit))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_user_summary(user_id):
    """Get income, expense, and savings summary for current month"""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    current_month = date.today().strftime("%Y-%m")
    
    cursor.execute("""
        SELECT type, SUM(amount) as total
        FROM transactions
        WHERE user_id=? AND date LIKE ?
        GROUP BY type
    """, (user_id, f"{current_month}%"))
    
    results = cursor.fetchall()
    conn.close()
    
    income = 0
    expense = 0
    for t_type, total in results:
        if t_type == 'income':
            income = total or 0
        elif t_type == 'expense':
            expense = total or 0
    
    savings = income - expense
    return {
        'income': income,
        'expense': expense,
        'savings': savings
    }

def get_all_user_transactions(user_id):
    """Get all transactions for a user"""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, type, category, amount, date, description
        FROM transactions
        WHERE user_id=?
        ORDER BY date DESC, id DESC
    """, (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_transaction_by_id(transaction_id, user_id=None):
    """Get a single transaction by ID"""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    if user_id:
        cursor.execute("""
            SELECT id, type, category, amount, date, description
            FROM transactions
            WHERE id=? AND user_id=?
        """, (transaction_id, user_id))
    else:
        cursor.execute("""
            SELECT id, type, category, amount, date, description
            FROM transactions
            WHERE id=?
        """, (transaction_id,))
    transaction = cursor.fetchone()
    conn.close()
    return transaction

def update_transaction(transaction_id, user_id, t_type, category, amount, description="", transaction_date=None):
    """Update an existing transaction"""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    if transaction_date:
        cursor.execute("""
            UPDATE transactions
            SET type=?, category=?, amount=?, date=?, description=?
            WHERE id=? AND user_id=?
        """, (t_type, category, amount, transaction_date, description, transaction_id, user_id))
    else:
        cursor.execute("""
            UPDATE transactions
            SET type=?, category=?, amount=?, description=?
            WHERE id=? AND user_id=?
        """, (t_type, category, amount, description, transaction_id, user_id))
    conn.commit()
    conn.close()
    print("✅ Transaction updated")
