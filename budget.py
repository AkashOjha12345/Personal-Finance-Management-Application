import sqlite3
from datetime import date

def set_budget(user_id, category, limit, month):
    """Set or update budget for a category in a month"""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    
    # Check if budget already exists
    cursor.execute("""
        SELECT id FROM budgets
        WHERE user_id=? AND category=? AND month=?
    """, (user_id, category, month))
    
    existing = cursor.fetchone()
    
    if existing:
        # Update existing budget
        cursor.execute("""
            UPDATE budgets
            SET monthly_limit=?
            WHERE user_id=? AND category=? AND month=?
        """, (limit, user_id, category, month))
    else:
        # Insert new budget
        cursor.execute("""
            INSERT INTO budgets (user_id, category, monthly_limit, month)
            VALUES (?, ?, ?, ?)
        """, (user_id, category, limit, month))
    
    conn.commit()
    conn.close()
    return True

def check_budget(user_id, category, month):
    """Check if budget is exceeded (console output)"""
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

def get_user_budgets(user_id, month=None):
    """Get all budgets for a user, optionally filtered by month"""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    
    if month:
        cursor.execute("""
            SELECT id, category, monthly_limit, month
            FROM budgets
            WHERE user_id=? AND month=?
            ORDER BY category
        """, (user_id, month))
    else:
        cursor.execute("""
            SELECT id, category, monthly_limit, month
            FROM budgets
            WHERE user_id=?
            ORDER BY month DESC, category
        """, (user_id,))
    
    budgets = cursor.fetchall()
    conn.close()
    return budgets

def get_budget_status(user_id, month=None):
    """Get budget status with spent amounts and warnings"""
    if month is None:
        month = date.today().strftime("%Y-%m")
    
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    
    # Get all budgets for the month
    cursor.execute("""
        SELECT category, monthly_limit
        FROM budgets
        WHERE user_id=? AND month=?
    """, (user_id, month))
    
    budgets = cursor.fetchall()
    
    budget_status = []
    for category, limit in budgets:
        # Get spent amount
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE user_id=? AND category=? AND type='expense' AND date LIKE ?
        """, (user_id, category, f"{month}%"))
        
        spent = cursor.fetchone()[0] or 0
        remaining = limit - spent
        percentage = (spent / limit * 100) if limit > 0 else 0
        exceeded = spent > limit
        
        budget_status.append({
            'category': category,
            'limit': limit,
            'spent': spent,
            'remaining': remaining,
            'percentage': percentage,
            'exceeded': exceeded
        })
    
    conn.close()
    return budget_status
