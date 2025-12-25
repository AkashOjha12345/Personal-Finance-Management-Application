"""
Test cases for authentication module
Tests user registration and login functionality
"""
import unittest
import sqlite3
import os
from auth import hash_password, register_user, login_user

class TestAuth(unittest.TestCase):
    """Test cases for authentication functions"""
    
    def setUp(self):
        """Set up test database"""
        self.test_db = "test_finance.db"
        # Remove test database if it exists
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        
        # Create test database
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def tearDown(self):
        """Clean up test database"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_password_hash(self):
        """Test that password is hashed and not stored as plain text"""
        password = "test123"
        hashed = hash_password(password)
        self.assertNotEqual(hashed, password)
        self.assertEqual(len(hashed), 64)  # SHA256 produces 64 char hex string
    
    def test_password_hash_consistency(self):
        """Test that same password produces same hash"""
        password = "test123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        self.assertEqual(hash1, hash2)
    
    def test_register_user_success(self):
        """Test successful user registration"""
        # Note: This test uses the actual database
        # In a real scenario, you'd mock the database connection
        result = register_user("testuser", "testpass")
        self.assertTrue(result)
    
    def test_register_duplicate_user(self):
        """Test that duplicate username registration fails"""
        register_user("duplicate_user", "pass1")
        result = register_user("duplicate_user", "pass2")
        self.assertFalse(result)
    
    def test_login_user_success(self):
        """Test successful user login"""
        register_user("loginuser", "loginpass")
        user_id = login_user("loginuser", "loginpass")
        self.assertIsNotNone(user_id)
    
    def test_login_user_wrong_password(self):
        """Test login with wrong password"""
        register_user("wrongpassuser", "correctpass")
        user_id = login_user("wrongpassuser", "wrongpass")
        self.assertIsNone(user_id)
    
    def test_login_user_nonexistent(self):
        """Test login with non-existent username"""
        user_id = login_user("nonexistent", "password")
        self.assertIsNone(user_id)

if __name__ == "__main__":
    unittest.main()
