# Personal Finance Management Application

A simple web application to manage your personal finances. Track income, expenses, set budgets, and view reports.

## Features

1. **User Registration and Login** - Create account and login securely
2. **Add Transactions** - Record income and expenses
3. **Edit/Delete Transactions** - Update or remove transactions
4. **View Reports** - See monthly and yearly financial summaries
5. **Set Budgets** - Set spending limits for categories
6. **Backup Data** - Save and restore your data

## Installation

1. Make sure Python is installed on your computer
2. Install Flask:
   ```
   pip install flask
   ```
3. Run the application:
   ```
   python main.py
   ```
4. Open your browser and go to: http://localhost:5000

## How to Use

1. **Register**: Create a new account with username and password
2. **Login**: Use your credentials to login
3. **Add Transaction**: Click "Add Transaction" to record income or expense
4. **View Dashboard**: See your income, expenses, and savings summary
5. **Edit/Delete**: Click Edit or Delete buttons on transactions
6. **Reports**: View monthly and yearly financial reports
7. **Budget**: Set monthly spending limits for categories
8. **Backup**: Create backup of your data or restore from backup

## Project Files

- `main.py` - Main application file with all routes and functions
- `templates/` - HTML pages
- `finance.db` - Database file (created automatically)

## Requirements

- Python 3.x
- Flask library

## Notes

- All data is stored in SQLite database (finance.db)
- Backup creates a copy named finance_backup.db
- Make sure to backup your data regularly
