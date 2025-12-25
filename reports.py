import sqlite3
from datetime import datetime

def monthly_report(user_id, month):
    """Generate monthly report (console output)"""
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

def get_monthly_report_data(user_id, month):
    """Get monthly report data for web display"""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Get income and expense totals
    cursor.execute("""
        SELECT type, SUM(amount) as total
        FROM transactions
        WHERE user_id=? AND date LIKE ?
        GROUP BY type
    """, (user_id, f"{month}%"))

    results = cursor.fetchall()
    
    income = 0
    expense = 0
    for t_type, total in results:
        if t_type == 'income':
            income = total or 0
        elif t_type == 'expense':
            expense = total or 0
    
    # Get transactions by category
    cursor.execute("""
        SELECT category, type, SUM(amount) as total
        FROM transactions
        WHERE user_id=? AND date LIKE ?
        GROUP BY category, type
        ORDER BY total DESC
    """, (user_id, f"{month}%"))
    
    category_data = cursor.fetchall()
    
    conn.close()
    
    return {
        'income': income,
        'expense': expense,
        'savings': income - expense,
        'category_data': category_data
    }

def yearly_report(user_id, year):
    """Generate yearly report (console output)"""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT type, SUM(amount)
        FROM transactions
        WHERE user_id=? AND date LIKE ?
        GROUP BY type
    """, (user_id, f"{year}%"))

    data = cursor.fetchall()
    conn.close()

    income = sum(a for t, a in data if t == 'income')
    expense = sum(a for t, a in data if t == 'expense')

    print(f"\n📊 Yearly Report ({year})")
    print(f"Income  : ₹{income}")
    print(f"Expense : ₹{expense}")
    print(f"Savings : ₹{income - expense}")

def get_yearly_report_data(user_id, year):
    """Get yearly report data for web display"""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Get income and expense totals
    cursor.execute("""
        SELECT type, SUM(amount) as total
        FROM transactions
        WHERE user_id=? AND date LIKE ?
        GROUP BY type
    """, (user_id, f"{year}%"))

    results = cursor.fetchall()
    
    income = 0
    expense = 0
    for t_type, total in results:
        if t_type == 'income':
            income = total or 0
        elif t_type == 'expense':
            expense = total or 0
    
    # Get monthly breakdown
    cursor.execute("""
        SELECT strftime('%Y-%m', date) as month, type, SUM(amount) as total
        FROM transactions
        WHERE user_id=? AND date LIKE ?
        GROUP BY month, type
        ORDER BY month
    """, (user_id, f"{year}%"))
    
    monthly_data = cursor.fetchall()
    
    conn.close()
    
    return {
        'income': income,
        'expense': expense,
        'savings': income - expense,
        'monthly_data': monthly_data
    }
