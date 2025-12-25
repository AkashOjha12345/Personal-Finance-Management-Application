import sqlite3

def set_budget(user_id, category, limit, month):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO budgets (user_id, category, monthly_limit, month)
        VALUES (?, ?, ?, ?)
    """, (user_id, category, limit, month))
    conn.commit()
    conn.close()

def check_budget(user_id, category, month):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT monthly_limit FROM budgets
        WHERE user_id=? AND category=? AND month=?
    """, (user_id, category, month))
    budget = cursor.fetchone()

    cursor.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id=? AND category=? AND type='expense' AND date LIKE ?
    """, (user_id, category, f"{month}%"))

    spent = cursor.fetchone()[0] or 0
    conn.close()

    if budget and spent > budget[0]:
        print(f"⚠️ Budget exceeded for {category}")
