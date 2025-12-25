from flask import Flask, render_template, request, redirect, session
from database import init_db
from auth import register_user, login_user
from transactions import add_transaction
from reports import monthly_report

app = Flask(__name__)
app.secret_key = "secret123"   # for session

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = login_user(
            request.form["username"],
            request.form["password"]
        )
        if user_id:
            session["user_id"] = user_id
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        register_user(
            request.form["username"],
            request.form["password"]
        )
        return redirect("/")
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        add_transaction(
            session["user_id"],
            request.form["type"],
            request.form["category"],
            float(request.form["amount"]),
            request.form["description"]
        )
        return redirect("/dashboard")
    return render_template("add_transaction.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
