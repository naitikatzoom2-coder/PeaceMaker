"""Account management for ATM simulator."""

from datetime import datetime


class Account:
    """Represents a bank account."""

    def __init__(self, account_number, pin, account_holder, balance=0.0):
        """Initialize an account.
        
        Args:
            account_number: Unique account identifier
            pin: Personal Identification Number (4 digits)
            account_holder: Name of account holder
            balance: Initial account balance (default: 0.0)
        """
        self.account_number = account_number
        self.pin = pin
        self.account_holder = account_holder
        self.balance = balance
        self.is_locked = False
        self.failed_attempts = 0
        self.max_failed_attempts = 3
        self.created_date = datetime.now()
        self.transactions = []

    def verify_pin(self, entered_pin):
        """Verify if entered PIN is correct.
        
        Args:
            entered_pin: PIN entered by user
            
        Returns:
            bool: True if PIN is correct, False otherwise
        """
        if self.is_locked:
            return False
        
        if str(entered_pin) == str(self.pin):
            self.failed_attempts = 0
            return True
        
        self.failed_attempts += 1
        if self.failed_attempts >= self.max_failed_attempts:
            self.is_locked = True
        
        return False

    def unlock_account(self):
        """Unlock the account (admin function)."""
        self.is_locked = False
        self.failed_attempts = 0

    def deposit(self, amount):
        """Deposit money into account.
        
        Args:
            amount: Amount to deposit
            
        Returns:
            bool: True if deposit successful, False otherwise
        """
        if amount <= 0:
            return False
        
        self.balance += amount
        transaction = {
            'type': 'DEPOSIT',
            'amount': amount,
            'balance_after': self.balance,
            'timestamp': datetime.now()
        }
        self.transactions.append(transaction)
        return True

    def withdraw(self, amount):
        """Withdraw money from account.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            bool: True if withdrawal successful, False otherwise
        """
        if amount <= 0:
            return False
        
        if amount > self.balance:
            return False
        
        self.balance -= amount
        transaction = {
            'type': 'WITHDRAWAL',
            'amount': amount,
            'balance_after': self.balance,
            'timestamp': datetime.now()
        }
        self.transactions.append(transaction)
        return True

    def change_pin(self, old_pin, new_pin):
        """Change account PIN.
        
        Args:
            old_pin: Current PIN
            new_pin: New PIN
            
        Returns:
            bool: True if PIN changed successfully, False otherwise
        """
        if not self.verify_pin(old_pin):
            return False
        
        if len(str(new_pin)) != 4 or not str(new_pin).isdigit():
            return False
        
        self.pin = new_pin
        return True

    def get_transaction_history(self, limit=5):
        """Get recent transactions.
        
        Args:
            limit: Number of recent transactions to return
            
        Returns:
            list: List of recent transactions
        """
        return self.transactions[-limit:]

    def get_balance(self):
        """Get current balance.
        
        Returns:
            float: Current account balance
        """
        return self.balance

    def __str__(self):
        """String representation of account."""
        return f"Account: {self.account_number} | Holder: {self.account_holder} | Balance: ${self.balance:.2f}"
