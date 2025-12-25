"""
Test cases for reports module
Tests monthly and yearly report generation
"""
import unittest
from datetime import date
from reports import get_monthly_report_data, get_yearly_report_data

class TestReports(unittest.TestCase):
    """Test cases for report functions"""
    
    def setUp(self):
        """Set up test data"""
        # Create a test user first
        from auth import register_user
        register_user("test_report_user", "testpass")
        from auth import login_user
        self.user_id = login_user("test_report_user", "testpass")
        
        # Add some test transactions
        from transactions import add_transaction
        current_month = date.today().strftime("%Y-%m")
        add_transaction(self.user_id, "income", "Salary", 10000.0, "Test income")
        add_transaction(self.user_id, "expense", "Food", 2000.0, "Test expense")
    
    def test_get_monthly_report_data(self):
        """Test getting monthly report data"""
        current_month = date.today().strftime("%Y-%m")
        data = get_monthly_report_data(self.user_id, current_month)
        
        self.assertIn('income', data)
        self.assertIn('expense', data)
        self.assertIn('savings', data)
        self.assertIn('category_data', data)
        self.assertIsInstance(data['income'], (int, float))
        self.assertIsInstance(data['expense'], (int, float))
        self.assertIsInstance(data['savings'], (int, float))
        self.assertIsInstance(data['category_data'], list)
    
    def test_get_yearly_report_data(self):
        """Test getting yearly report data"""
        current_year = date.today().strftime("%Y")
        data = get_yearly_report_data(self.user_id, current_year)
        
        self.assertIn('income', data)
        self.assertIn('expense', data)
        self.assertIn('savings', data)
        self.assertIn('monthly_data', data)
        self.assertIsInstance(data['income'], (int, float))
        self.assertIsInstance(data['expense'], (int, float))
        self.assertIsInstance(data['savings'], (int, float))
        self.assertIsInstance(data['monthly_data'], list)
    
    def test_monthly_report_calculation(self):
        """Test that monthly report calculates correctly"""
        current_month = date.today().strftime("%Y-%m")
        data = get_monthly_report_data(self.user_id, current_month)
        
        # Savings should be income - expense
        expected_savings = data['income'] - data['expense']
        self.assertEqual(data['savings'], expected_savings)

if __name__ == "__main__":
    unittest.main()

