import unittest
from auth import hash_password

class TestAuth(unittest.TestCase):
    def test_password_hash(self):
        self.assertNotEqual(hash_password("123"), "123")

if __name__ == "__main__":
    unittest.main()
