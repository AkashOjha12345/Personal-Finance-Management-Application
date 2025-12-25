"""
Test cases for budget module
Tests budget setting and checking functionality
"""
import unittest
from datetime import date
from budget import set_budget, get_user_budgets, get_budget_status

class TestBudget(unittest.TestCase):
    """Test cases for budget functions"""
    
    def setUp(self):
        """Set up test data"""
        # Create a test user first
        from auth import register_user
        register_user("test_budget_user", "testpass")
        from auth import login_user
        self.user_id = login_user("test_budget_user", "testpass")
        
        # Add some test transactions
        from transactions import add_transaction
        current_month = date.today().strftime("%Y-%m")
        add_transaction(self.user_id, "expense", "Food", 1500.0, "Test expense")
    
    def test_set_budget(self):
        """Test setting a budget"""
        current_month = date.today().strftime("%Y-%m")
        try:
            result = set_budget(self.user_id, "Food", 2000.0, current_month)
            self.assertTrue(result)
        except Exception as e:
            self.fail(f"set_budget raised an exception: {e}")
    
    def test_get_user_budgets(self):
        """Test getting user budgets"""
        current_month = date.today().strftime("%Y-%m")
        set_budget(self.user_id, "Food", 2000.0, current_month)
        budgets = get_user_budgets(self.user_id, current_month)
        
        self.assertIsInstance(budgets, list)
        if budgets:
            self.assertEqual(len(budgets[0]), 4)  # id, category, limit, month
    
    def test_get_budget_status(self):
        """Test getting budget status"""
        current_month = date.today().strftime("%Y-%m")
        set_budget(self.user_id, "Food", 2000.0, current_month)
        status = get_budget_status(self.user_id, current_month)
        
        self.assertIsInstance(status, list)
        if status:
            budget = status[0]
            self.assertIn('category', budget)
            self.assertIn('limit', budget)
            self.assertIn('spent', budget)
            self.assertIn('remaining', budget)
            self.assertIn('percentage', budget)
            self.assertIn('exceeded', budget)

if __name__ == "__main__":
    unittest.main()

