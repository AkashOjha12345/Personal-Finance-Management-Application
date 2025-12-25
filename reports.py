import sqlite3

def monthly_report(user_id, month):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT type, SUM(amount)
        FROM transactions
        WHERE user_id=? AND date LIKE ?
        GROUP BY type
    """, (user_id, f"{month}%"))

    data = cursor.fetchall()
    conn.close()

    income = sum(a for t, a in data if t == 'income')
    expense = sum(a for t, a in data if t == 'expense')

    print(f"\n📊 Monthly Report ({month})")
    print(f"Income  : ₹{income}")
    print(f"Expense : ₹{expense}")
    print(f"Savings : ₹{income - expense}")
