# Personal Finance Management Application
# Simple version for beginners

from flask import Flask, render_template, request, redirect, session
import sqlite3
import hashlib
import re
from datetime import date

app = Flask(__name__)
app.secret_key = "secret123"

# Create database tables
def create_tables():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    
    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        # Check what columns exist in users table
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # If table has 'username' but not 'email', migrate it
        if 'username' in columns and 'email' not in columns:
            try:
                # Create new table with email column
                cursor.execute("""
                    CREATE TABLE users_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE,
                        password TEXT
                    )
                """)
                # Copy data: use username values as email
                cursor.execute("INSERT INTO users_new (id, email, password) SELECT id, username, password FROM users")
                # Drop old table
                cursor.execute("DROP TABLE users")
                # Rename new table
                cursor.execute("ALTER TABLE users_new RENAME TO users")
                conn.commit()
            except Exception as e:
                print(f"Migration error: {e}")
                conn.rollback()
    
    # Create users table if it doesn't exist (with email column)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    
    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            category TEXT,
            amount REAL,
            date TEXT,
            description TEXT
        )
    """)
    
    # Budgets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT,
            monthly_limit REAL,
            month TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize database
create_tables()

# Email validation
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Home page - Login
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    success = None
    
    # Check if user just registered
    if request.args.get("registered") == "1":
        success = "Registration successful! Please login with your email and password."
    
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        
        # Validate input fields
        if not email:
            error = "Please enter your email address"
        elif not is_valid_email(email):
            error = "Please enter a valid email address"
        elif not password:
            error = "Please enter your password"
        else:
            # Check if email exists
            conn = sqlite3.connect("finance.db")
            cursor = conn.cursor()
            
            # First check if email exists
            cursor.execute("SELECT id, password FROM users WHERE email=?", (email,))
            user = cursor.fetchone()
            
            if not user:
                error = "Email address not found. Please register first."
            else:
                # Check password
                if user[1] == hash_password(password):
                    session["user_id"] = user[0]
                    conn.close()
                    return redirect("/dashboard")
                else:
                    error = "Incorrect password. Please try again."
            
            conn.close()
    
    return render_template("login.html", error=error, success=success)

# Forgot Password page
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    error = None
    success = None
    email = None
    
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        
        if not email:
            error = "Please enter your email address"
        elif not is_valid_email(email):
            error = "Please enter a valid email address"
        else:
            # Check if email exists
            conn = sqlite3.connect("finance.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email=?", (email,))
            user = cursor.fetchone()
            
            if not user:
                error = "Email address not found in our system"
                conn.close()
            else:
                # Check if this is password reset request
                if "new_password" in request.form:
                    new_password = request.form.get("new_password", "").strip()
                    confirm_password = request.form.get("confirm_password", "").strip()
                    
                    if not new_password:
                        error = "Please enter a new password"
                    elif len(new_password) < 4:
                        error = "Password must be at least 4 characters long"
                    elif new_password != confirm_password:
                        error = "Passwords do not match"
                    else:
                        # Update password
                        cursor.execute(
                            "UPDATE users SET password=? WHERE email=?",
                            (hash_password(new_password), email)
                        )
                        conn.commit()
                        conn.close()
                        success = "Password reset successfully! You can now login with your new password."
                        email = None  # Clear email after successful reset
                else:
                    # Email exists, show reset form
                    conn.close()
                    return render_template("forgot_password.html", 
                                         error=error, 
                                         success=success, 
                                         email=email,
                                         show_reset_form=True)
    
    return render_template("forgot_password.html", 
                         error=error, 
                         success=success, 
                         email=email,
                         show_reset_form=False)

# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        
        # Validate all fields
        if not email:
            error = "Please enter your email address"
        elif not is_valid_email(email):
            error = "Please enter a valid email address (e.g., user@example.com)"
        elif not password:
            error = "Please enter a password"
        elif len(password) < 4:
            error = "Password must be at least 4 characters long"
        elif not confirm_password:
            error = "Please confirm your password"
        elif password != confirm_password:
            error = "Passwords do not match. Please try again."
        else:
            # Check if email already exists
            conn = sqlite3.connect("finance.db")
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM users WHERE email=?", (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                error = "This email address is already registered. Please login instead."
                conn.close()
            else:
                # Create new account
                try:
                    cursor.execute(
                        "INSERT INTO users (email, password) VALUES (?, ?)",
                        (email, hash_password(password))
                    )
                    conn.commit()
                    conn.close()
                    # Redirect to login with success message
                    return redirect("/?registered=1")
                except Exception as e:
                    error = "Registration failed. Please try again."
                    conn.close()
    
    return render_template("register.html", error=error)

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    
    # Get current month summary
    current_month = date.today().strftime("%Y-%m")
    cursor.execute("""
        SELECT type, SUM(amount) FROM transactions
        WHERE user_id=? AND date LIKE ?
        GROUP BY type
    """, (user_id, f"{current_month}%"))
    
    results = cursor.fetchall()
    income = 0
    expense = 0
    for row in results:
        if row[0] == "income":
            income = row[1] or 0
        elif row[0] == "expense":
            expense = row[1] or 0
    
    savings = income - expense
    
    # Get recent transactions
    cursor.execute("""
        SELECT id, type, category, amount, date, description
        FROM transactions
        WHERE user_id=?
        ORDER BY date DESC
        LIMIT 10
    """, (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    
    return render_template("dashboard.html", 
                         income=income, 
                         expense=expense, 
                         savings=savings,
                         transactions=transactions)

# Add transaction
@app.route("/add", methods=["GET", "POST"])
def add():
    if "user_id" not in session:
        return redirect("/")
    
    if request.method == "POST":
        user_id = session["user_id"]
        t_type = request.form["type"]
        category = request.form["category"]
        amount = float(request.form["amount"])
        description = request.form.get("description", "")
        
        conn = sqlite3.connect("finance.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (user_id, type, category, amount, date, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, t_type, category, amount, str(date.today()), description))
        conn.commit()
        conn.close()
        
        return redirect("/dashboard")
    
    return render_template("add_transaction.html")

# Edit transaction
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit(transaction_id):
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    
    if request.method == "POST":
        cursor.execute("""
            UPDATE transactions
            SET type=?, category=?, amount=?, description=?
            WHERE id=? AND user_id=?
        """, (request.form["type"], request.form["category"], 
              float(request.form["amount"]), request.form.get("description", ""),
              transaction_id, user_id))
        conn.commit()
        conn.close()
        return redirect("/dashboard")
    
    cursor.execute("""
        SELECT id, type, category, amount, date, description
        FROM transactions
        WHERE id=? AND user_id=?
    """, (transaction_id, user_id))
    transaction = cursor.fetchone()
    conn.close()
    
    if not transaction:
        return redirect("/dashboard")
    
    return render_template("edit_transaction.html", transaction=transaction)

# Delete transaction
@app.route("/delete/<int:transaction_id>")
def delete(transaction_id):
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=? AND user_id=?", 
                  (transaction_id, user_id))
    conn.commit()
    conn.close()
    
    return redirect("/dashboard")

# Reports
@app.route("/reports")
def reports():
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    month = request.args.get("month", date.today().strftime("%Y-%m"))
    year = request.args.get("year", date.today().strftime("%Y"))
    
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    
    # Monthly report
    cursor.execute("""
        SELECT type, SUM(amount) FROM transactions
        WHERE user_id=? AND date LIKE ?
        GROUP BY type
    """, (user_id, f"{month}%"))
    
    monthly_results = cursor.fetchall()
    monthly_income = 0
    monthly_expense = 0
    for row in monthly_results:
        if row[0] == "income":
            monthly_income = row[1] or 0
        elif row[0] == "expense":
            monthly_expense = row[1] or 0
    
    # Yearly report
    cursor.execute("""
        SELECT type, SUM(amount) FROM transactions
        WHERE user_id=? AND date LIKE ?
        GROUP BY type
    """, (user_id, f"{year}%"))
    
    yearly_results = cursor.fetchall()
    yearly_income = 0
    yearly_expense = 0
    for row in yearly_results:
        if row[0] == "income":
            yearly_income = row[1] or 0
        elif row[0] == "expense":
            yearly_expense = row[1] or 0
    
    conn.close()
    
    return render_template("reports.html",
                         month=month,
                         year=year,
                         monthly_income=monthly_income,
                         monthly_expense=monthly_expense,
                         monthly_savings=monthly_income - monthly_expense,
                         yearly_income=yearly_income,
                         yearly_expense=yearly_expense,
                         yearly_savings=yearly_income - yearly_expense)

# Budget
@app.route("/budget", methods=["GET", "POST"])
def budget():
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    month = request.args.get("month", date.today().strftime("%Y-%m"))
    
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    
    if request.method == "POST":
        category = request.form["category"]
        limit = float(request.form["limit"])
        month = request.form["month"]
        
        # Check if budget exists
        cursor.execute("""
            SELECT id FROM budgets
            WHERE user_id=? AND category=? AND month=?
        """, (user_id, category, month))
        
        if cursor.fetchone():
            cursor.execute("""
                UPDATE budgets SET monthly_limit=?
                WHERE user_id=? AND category=? AND month=?
            """, (limit, user_id, category, month))
        else:
            cursor.execute("""
                INSERT INTO budgets (user_id, category, monthly_limit, month)
                VALUES (?, ?, ?, ?)
            """, (user_id, category, limit, month))
        
        conn.commit()
        conn.close()
        return redirect(f"/budget?month={month}")
    
    # Get budgets for the month
    cursor.execute("""
        SELECT category, monthly_limit FROM budgets
        WHERE user_id=? AND month=?
    """, (user_id, month))
    budgets = cursor.fetchall()
    
    # Get budget status
    budget_list = []
    for category, limit in budgets:
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) FROM transactions
            WHERE user_id=? AND category=? AND type='expense' AND date LIKE ?
        """, (user_id, category, f"{month}%"))
        spent = cursor.fetchone()[0] or 0
        budget_list.append({
            "category": category,
            "limit": limit,
            "spent": spent,
            "remaining": limit - spent
        })
    
    conn.close()
    
    return render_template("budget.html", budgets=budget_list, month=month)

# Backup
@app.route("/backup", methods=["GET", "POST"])
def backup():
    if "user_id" not in session:
        return redirect("/")
    
    message = None
    if request.method == "POST":
        import shutil
        if request.form["action"] == "backup":
            shutil.copy("finance.db", "finance_backup.db")
            message = "Backup created!"
        elif request.form["action"] == "restore":
            shutil.copy("finance_backup.db", "finance.db")
            message = "Backup restored!"
    
    return render_template("backup.html", message=message)

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
