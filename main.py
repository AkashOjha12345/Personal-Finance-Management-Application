from flask import Flask, render_template, request, redirect, session
from datetime import date
from database import init_db
from auth import register_user, login_user
from transactions import add_transaction, get_user_transactions, get_user_summary, delete_transaction, get_all_user_transactions, get_transaction_by_id, update_transaction
from reports import monthly_report, yearly_report, get_monthly_report_data, get_yearly_report_data
from budget import set_budget, check_budget, get_user_budgets, get_budget_status
from backup import backup_db, restore_db

app = Flask(__name__)
app.secret_key = "secret123"   # for session

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user_id = login_user(
            request.form["username"],
            request.form["password"]
        )
        if user_id:
            session["user_id"] = user_id
            return redirect("/dashboard")
        else:
            error = "Invalid username or password. Please try again."
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    success = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        
        # Validation
        if not username or len(username) < 3:
            error = "Username must be at least 3 characters long."
        elif not password or len(password) < 4:
            error = "Password must be at least 4 characters long."
        elif password != confirm_password:
            error = "Passwords do not match. Please try again."
        else:
            if register_user(username, password):
                success = "Registration successful! Redirecting to login..."
                # Redirect after a short delay to show success message
                return render_template("register.html", success=success)
            else:
                error = "Username already exists. Please choose a different username."
    
    return render_template("register.html", error=error, success=success)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    summary = get_user_summary(user_id)
    recent_transactions = get_user_transactions(user_id, limit=10)
    
    return render_template("dashboard.html", 
                         summary=summary, 
                         transactions=recent_transactions)

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user_id" not in session:
        return redirect("/")
    
    if request.method == "POST":
        add_transaction(
            session["user_id"],
            request.form["type"],
            request.form["category"],
            float(request.form["amount"]),
            request.form.get("description", "")
        )
        return redirect("/dashboard")
    return render_template("add_transaction.html")

@app.route("/edit_transaction/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    transaction = get_transaction_by_id(transaction_id, user_id)
    
    if not transaction:
        return redirect("/dashboard")
    
    if request.method == "POST":
        update_transaction(
            transaction_id,
            user_id,
            request.form["type"],
            request.form["category"],
            float(request.form["amount"]),
            request.form.get("description", ""),
            request.form.get("date", transaction[4])
        )
        return redirect("/dashboard")
    
    return render_template("edit_transaction.html", transaction=transaction)

@app.route("/delete_transaction/<int:transaction_id>")
def delete_trans(transaction_id):
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]
    delete_transaction(transaction_id, user_id)
    return redirect("/dashboard")

@app.route("/reports")
def reports():
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    current_month = date.today().strftime("%Y-%m")
    current_year = date.today().strftime("%Y")
    
    # Get selected month/year from query params
    selected_month = request.args.get("month", current_month)
    selected_year = request.args.get("year", current_year)
    
    monthly_data = get_monthly_report_data(user_id, selected_month)
    yearly_data = get_yearly_report_data(user_id, selected_year)
    
    return render_template("reports.html", 
                         monthly_data=monthly_data,
                         yearly_data=yearly_data,
                         selected_month=selected_month,
                         selected_year=selected_year)

@app.route("/budget", methods=["GET", "POST"])
def budget():
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    current_month = date.today().strftime("%Y-%m")
    selected_month = request.args.get("month", current_month)
    
    if request.method == "POST":
        set_budget(
            user_id,
            request.form["category"],
            float(request.form["limit"]),
            request.form["month"]
        )
        return redirect(f"/budget?month={request.form['month']}")
    
    budgets = get_user_budgets(user_id, selected_month)
    budget_status = get_budget_status(user_id, selected_month)
    
    return render_template("budget.html",
                         budgets=budgets,
                         budget_status=budget_status,
                         selected_month=selected_month)

@app.route("/backup", methods=["GET", "POST"])
def backup():
    if "user_id" not in session:
        return redirect("/")
    
    message = None
    if request.method == "POST":
        action = request.form.get("action")
        if action == "backup":
            try:
                backup_db()
                message = "Backup created successfully!"
            except Exception as e:
                message = f"Error creating backup: {str(e)}"
        elif action == "restore":
            try:
                restore_db()
                message = "Database restored successfully!"
            except Exception as e:
                message = f"Error restoring backup: {str(e)}"
    
    return render_template("backup.html", message=message)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
