# tests/test_users.py

import unittest
import sys
import os

# 1) Aseguramos que 'src/' esté en import path:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.users import validate_email, validate_password, register_user

class TestUsers(unittest.TestCase):

    def test_validations(self):
        email_cases = {
            "user@example.com": True,
            "bad-email":        False,
        }
        password_cases = {
            "Aa1!aaaa": True,
            "short1!":  False,
        }

        for email, expect in email_cases.items():
            with self.subTest(email=email):
                self.assertEqual(validate_email(email), expect)

        for pw, expect in password_cases.items():
            with self.subTest(password=pw):
                self.assertEqual(validate_password(pw), expect)

    def test_register_duplicate_raises(self):
        users = []
        # 1ª inserción OK
        self.assertTrue(register_user(users, "Alice", "a@b.com", "Aa1!aaaa"))
        # 2ª con mismo email → ValueError
        with self.assertRaises(ValueError):
            register_user(users, "Bob", "a@b.com", "Aa1!aaaa")


if __name__ == "__main__":
    unittest.main()
