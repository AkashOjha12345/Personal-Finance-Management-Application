# Personal Finance Management Application

A simple and user-friendly web application to manage your personal finances. Track your income, expenses, set budgets, and generate financial reports - all in one place!

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## ✨ Features

### 1. User Registration and Authentication
- **User Registration**: Create a new account with a unique username and secure password
- **User Login**: Secure login system with password hashing
- **Session Management**: Automatic session handling for logged-in users

### 2. Income and Expense Tracking
- **Add Transactions**: Record income and expense entries with categories
- **Edit Transactions**: Update existing transaction details
- **Delete Transactions**: Remove unwanted transactions
- **Transaction Categories**: Organize transactions by categories (Food, Rent, Salary, etc.)
- **Transaction History**: View all your transactions in one place

### 3. Financial Reports
- **Monthly Reports**: View income, expenses, and savings for any month
- **Yearly Reports**: Get annual financial overview
- **Category Breakdown**: See spending patterns by category
- **Visual Summary**: Easy-to-read summary cards

### 4. Budgeting
- **Set Monthly Budgets**: Define spending limits for different categories
- **Budget Tracking**: Monitor your spending against set budgets
- **Budget Warnings**: Get notified when you exceed budget limits
- **Progress Indicators**: Visual progress bars showing budget usage

### 5. Data Persistence
- **SQLite Database**: All data stored in a local SQLite database
- **Backup Functionality**: Create backups of your financial data
- **Restore Functionality**: Restore data from previous backups

### 6. Beautiful User Interface
- **Modern Design**: Clean and intuitive interface
- **Responsive Layout**: Works on desktop and mobile devices
- **Interactive Elements**: Smooth animations and transitions
- **Color-Coded Information**: Easy visual distinction between income and expenses

## 📦 Requirements

Before installing, make sure you have the following installed on your system:

- **Python 3.7 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package installer) - Usually comes with Python

## 🚀 Installation

Follow these steps to set up the application on your computer:

### Step 1: Download the Project

1. Download or clone this project to your computer
2. Navigate to the project folder using Command Prompt (Windows) or Terminal (Mac/Linux)

### Step 2: Install Dependencies

The application uses Flask web framework. Install it using pip:

```bash
pip install flask
```

**For Windows:**
```bash
python -m pip install flask
```

**For Mac/Linux:**
```bash
pip3 install flask
```

### Step 3: Verify Installation

Check if Flask is installed correctly:

```bash
python -c "import flask; print(flask.__version__)"
```

You should see the Flask version number.

## 💻 Usage

### Starting the Application

1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Navigate to the project folder:
   ```bash
   cd path/to/Personal-Finance-Management-Application
   ```
3. Run the application:
   ```bash
   python main.py
   ```
   
   Or on some systems:
   ```bash
   python3 main.py
   ```

4. You should see output like:
   ```
   * Running on http://127.0.0.1:5000
   ```

### Accessing the Application

1. Open your web browser (Chrome, Firefox, Safari, etc.)
2. Go to: `http://localhost:5000` or `http://127.0.0.1:5000`
3. You should see the login page

### Using the Application

#### 1. Create an Account
- Click on "Create one now" or go to `/register`
- Enter a username (at least 3 characters)
- Enter a password (at least 4 characters)
- Confirm your password
- Click "Create Account"

#### 2. Login
- Enter your username and password
- Click "Sign In"
- You'll be redirected to the dashboard

#### 3. Add a Transaction
- Click "Add Transaction" button on the dashboard
- Select transaction type (Income or Expense)
- Enter category (e.g., Salary, Food, Rent)
- Enter amount
- Add optional description
- Click "Add Transaction"

#### 4. View Dashboard
- See summary cards showing:
  - Total Income (this month)
  - Total Expenses (this month)
  - Savings (Income - Expenses)
- View recent transactions
- Edit or delete transactions

#### 5. View Reports
- Click "Reports" button
- Select a month to view monthly report
- Select a year to view yearly report
- See breakdown by categories

#### 6. Set Budgets
- Click "Budget" button
- Enter category name
- Set monthly limit
- Select month
- Click "Set Budget"
- View budget status with progress indicators

#### 7. Backup Data
- Click "Backup" button (if available in navigation)
- Click "Create Backup" to save your data
- Click "Restore Backup" to restore from backup

#### 8. Logout
- Click "Logout" button
- You'll be redirected to login page

## 📁 Project Structure

```
Personal-Finance-Management-Application/
│
├── main.py                 # Main Flask application file
├── database.py            # Database initialization
├── auth.py                # User authentication functions
├── transactions.py       # Transaction management functions
├── reports.py             # Report generation functions
├── budget.py              # Budget management functions
├── backup.py              # Backup and restore functions
│
├── templates/             # HTML templates
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # Main dashboard
│   ├── add_transaction.html  # Add transaction form
│   ├── edit_transaction.html # Edit transaction form
│   ├── reports.html       # Reports page
│   ├── budget.html        # Budget management page
│   └── backup.html        # Backup/restore page
│
├── static/                # Static files (CSS, JS, images)
│   └── style.css         # Global styles
│
├── tests/                 # Test files
│   ├── test_auth.py       # Authentication tests
│   ├── test_transactions.py # Transaction tests
│   ├── test_reports.py    # Report tests
│   └── test_budget.py    # Budget tests
│
├── finance.db             # SQLite database (created automatically)
└── README.md              # This file
```

## 🧪 Testing

Run tests to verify everything works correctly:

### Run All Tests

```bash
python -m unittest discover tests
```

### Run Individual Test Files

```bash
# Test authentication
python -m unittest tests.test_auth

# Test transactions
python -m unittest tests.test_transactions

# Test reports
python -m unittest tests.test_reports

# Test budget
python -m unittest tests.test_budget
```

## 🔧 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Solution:** Install Flask:
```bash
pip install flask
```

### Problem: "Address already in use"

**Solution:** Another instance is running. Close it or change the port in `main.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Problem: "Database is locked"

**Solution:** Close any other programs accessing the database. Restart the application.

### Problem: Can't login after registration

**Solution:** 
- Make sure you're using the correct username and password
- Check if the database file (finance.db) exists
- Try registering again with a different username

### Problem: Page not loading

**Solution:**
- Make sure the application is running (check terminal/command prompt)
- Try refreshing the page (F5 or Ctrl+R)
- Clear browser cache
- Check the URL is correct: `http://localhost:5000`

## 📝 Code Explanation (For Students)

### How It Works

1. **Flask Framework**: Flask is a web framework that helps create web applications in Python. It handles HTTP requests and responses.

2. **Database (SQLite)**: SQLite is a lightweight database that stores data in a file (`finance.db`). It's perfect for small applications.

3. **Sessions**: Flask sessions store user login information temporarily. When you log in, your user ID is stored in the session.

4. **Templates**: HTML templates (in `templates/` folder) are used to create web pages. Flask uses Jinja2 template engine to insert dynamic data.

5. **Routes**: Routes (like `/dashboard`, `/add`) define what happens when you visit different URLs.

### Key Functions

- **`register_user()`**: Creates a new user account
- **`login_user()`**: Verifies username and password
- **`add_transaction()`**: Saves a new transaction to database
- **`get_user_summary()`**: Calculates income, expenses, and savings
- **`set_budget()`**: Sets spending limit for a category
- **`backup_db()`**: Creates a backup of the database

## 🎯 Future Enhancements

Ideas for improving the application:

1. **Charts and Graphs**: Add visual charts for better data visualization
2. **Export to CSV/PDF**: Export reports to files
3. **Email Notifications**: Send budget alerts via email
4. **Multiple Currencies**: Support for different currencies
5. **Recurring Transactions**: Automatically add recurring expenses
6. **Goals**: Set and track financial goals
7. **Categories Management**: Add/edit/delete categories
8. **Search and Filter**: Search transactions by date, category, etc.

## 📚 Learning Resources

For students who want to learn more:

- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLite Tutorial**: https://www.sqlitetutorial.net/
- **Python Basics**: https://www.python.org/about/gettingstarted/
- **HTML/CSS**: https://www.w3schools.com/

## 👨‍💻 For Developers

### Adding New Features

1. Create a new function in the appropriate module (e.g., `transactions.py`)
2. Add a route in `main.py`
3. Create an HTML template in `templates/`
4. Test your changes

### Database Schema

**Users Table:**
- id (INTEGER, PRIMARY KEY)
- username (TEXT, UNIQUE)
- password (TEXT, hashed)

**Transactions Table:**
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER)
- type (TEXT: 'income' or 'expense')
- category (TEXT)
- amount (REAL)
- date (TEXT)
- description (TEXT)

**Budgets Table:**
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER)
- category (TEXT)
- monthly_limit (REAL)
- month (TEXT)

## 📄 License

This project is created for educational purposes. Feel free to use and modify as needed.

## 🤝 Contributing

This is a learning project. Feel free to:
- Report bugs
- Suggest improvements
- Add new features
- Improve documentation

## 📧 Support

If you encounter any issues or have questions:
1. Check the Troubleshooting section
2. Review the code comments
3. Check Flask and SQLite documentation

---

**Happy Learning! 🎓**

