"""
Test cases for transactions module
Tests transaction add, update, delete, and retrieval functions
"""
import unittest
import sqlite3
import os
from datetime import date
from transactions import add_transaction, get_user_transactions, get_user_summary, delete_transaction, update_transaction, get_transaction_by_id

class TestTransactions(unittest.TestCase):
    """Test cases for transaction functions"""
    
    def setUp(self):
        """Set up test data"""
        # Create a test user first
        from auth import register_user
        register_user("test_trans_user", "testpass")
        from auth import login_user
        self.user_id = login_user("test_trans_user", "testpass")
    
    def test_add_transaction(self):
        """Test adding a transaction"""
        # This will add to the actual database
        # In production, use a test database
        try:
            add_transaction(self.user_id, "income", "Salary", 5000.0, "Monthly salary")
            # If no exception, test passed
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"add_transaction raised an exception: {e}")
    
    def test_get_user_transactions(self):
        """Test retrieving user transactions"""
        add_transaction(self.user_id, "expense", "Food", 500.0, "Lunch")
        transactions = get_user_transactions(self.user_id, limit=10)
        self.assertIsInstance(transactions, list)
    
    def test_get_user_summary(self):
        """Test getting user summary"""
        summary = get_user_summary(self.user_id)
        self.assertIn('income', summary)
        self.assertIn('expense', summary)
        self.assertIn('savings', summary)
        self.assertIsInstance(summary['income'], (int, float))
        self.assertIsInstance(summary['expense'], (int, float))
        self.assertIsInstance(summary['savings'], (int, float))
    
    def test_delete_transaction(self):
        """Test deleting a transaction"""
        # Add a transaction first
        add_transaction(self.user_id, "expense", "Test", 100.0, "Test transaction")
        transactions = get_user_transactions(self.user_id, limit=1)
        if transactions:
            transaction_id = transactions[0][0]
            try:
                delete_transaction(transaction_id, self.user_id)
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"delete_transaction raised an exception: {e}")
    
    def test_update_transaction(self):
        """Test updating a transaction"""
        # Add a transaction first
        add_transaction(self.user_id, "expense", "Original", 100.0, "Original description")
        transactions = get_user_transactions(self.user_id, limit=1)
        if transactions:
            transaction_id = transactions[0][0]
            try:
                update_transaction(transaction_id, self.user_id, "expense", "Updated", 200.0, "Updated description")
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"update_transaction raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()

