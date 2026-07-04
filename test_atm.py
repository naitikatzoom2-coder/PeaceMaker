"""Unit tests for ATM Simulator."""

import unittest
import os
from atm import ATM
from account import Account
from transaction import Transaction


class TestAccount(unittest.TestCase):
    """Test Account class."""

    def setUp(self):
        """Set up test account."""
        self.account = Account("1001", "1234", "John Doe", 5000.00)

    def test_account_creation(self):
        """Test account creation."""
        self.assertEqual(self.account.account_number, "1001")
        self.assertEqual(self.account.account_holder, "John Doe")
        self.assertEqual(self.account.balance, 5000.00)

    def test_deposit(self):
        """Test deposit operation."""
        self.assertTrue(self.account.deposit(100))
        self.assertEqual(self.account.balance, 5100.00)

    def test_withdraw(self):
        """Test withdrawal operation."""
        self.assertTrue(self.account.withdraw(500))
        self.assertEqual(self.account.balance, 4500.00)

    def test_insufficient_balance(self):
        """Test withdrawal with insufficient balance."""
        self.assertFalse(self.account.withdraw(10000))
        self.assertEqual(self.account.balance, 5000.00)

    def test_verify_pin(self):
        """Test PIN verification."""
        self.assertTrue(self.account.verify_pin("1234"))
        self.assertFalse(self.account.verify_pin("9999"))

    def test_change_pin(self):
        """Test PIN change."""
        self.assertTrue(self.account.change_pin("1234", "5678"))
        self.assertTrue(self.account.verify_pin("5678"))
        self.assertFalse(self.account.verify_pin("1234"))


class TestTransaction(unittest.TestCase):
    """Test Transaction class."""

    def test_transaction_creation(self):
        """Test transaction creation."""
        txn = Transaction("1001", "WITHDRAWAL", 100.00, 4900.00, "Test withdrawal")
        self.assertEqual(txn.account_number, "1001")
        self.assertEqual(txn.transaction_type, "WITHDRAWAL")
        self.assertEqual(txn.amount, 100.00)


class TestATM(unittest.TestCase):
    """Test ATM class."""

    def setUp(self):
        """Set up test ATM."""
        # Use test database
        self.atm = ATM('test_atm.db')
        self.atm.create_account("2001", "1234", "Test User", 5000.00)

    def tearDown(self):
        """Clean up after tests."""
        self.atm.db.close()
        if os.path.exists('test_atm.db'):
            os.remove('test_atm.db')

    def test_create_account(self):
        """Test account creation."""
        result = self.atm.create_account("2002", "5678", "Another User", 1000.00)
        self.assertTrue(result)

    def test_duplicate_account(self):
        """Test duplicate account creation."""
        result = self.atm.create_account("2001", "9999", "Duplicate", 0)
        self.assertFalse(result)

    def test_login_success(self):
        """Test successful login."""
        result = self.atm.login("2001", "1234")
        self.assertTrue(result)
        self.assertIsNotNone(self.atm.current_account)

    def test_login_failure(self):
        """Test login with wrong PIN."""
        result = self.atm.login("2001", "9999")
        self.assertFalse(result)

    def test_check_balance(self):
        """Test balance check."""
        self.atm.login("2001", "1234")
        balance = self.atm.check_balance()
        self.assertEqual(balance, 5000.00)

    def test_deposit_operation(self):
        """Test deposit."""
        self.atm.login("2001", "1234")
        self.assertTrue(self.atm.deposit(500))
        self.assertEqual(self.atm.current_account.balance, 5500.00)

    def test_withdraw_operation(self):
        """Test withdrawal."""
        self.atm.login("2001", "1234")
        self.assertTrue(self.atm.withdraw(1000))
        self.assertEqual(self.atm.current_account.balance, 4000.00)


if __name__ == '__main__':
    unittest.main()
