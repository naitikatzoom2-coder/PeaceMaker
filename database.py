"""Database management for ATM simulator."""

import sqlite3
import json
from datetime import datetime


class Database:
    """SQLite database for storing accounts and transactions."""

    def __init__(self, db_name='atm.db'):
        """Initialize database connection.
        
        Args:
            db_name: Name of SQLite database file
        """
        self.db_name = db_name
        self.connection = None
        self.init_database()

    def init_database(self):
        """Initialize database tables."""
        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()

        # Create accounts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_number TEXT PRIMARY KEY,
                pin TEXT NOT NULL,
                account_holder TEXT NOT NULL,
                balance REAL NOT NULL,
                is_locked INTEGER DEFAULT 0,
                created_date TEXT NOT NULL,
                updated_date TEXT NOT NULL
            )
        ''')

        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                account_number TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                balance_after REAL NOT NULL,
                description TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (account_number) REFERENCES accounts(account_number)
            )
        ''')

        self.connection.commit()

    def add_account(self, account_number, pin, account_holder, balance=0.0):
        """Add a new account to database.
        
        Args:
            account_number: Unique account number
            pin: Personal identification number
            account_holder: Name of account holder
            balance: Initial balance
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO accounts (account_number, pin, account_holder, balance, created_date, updated_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (account_number, pin, account_holder, balance, datetime.now().isoformat(), datetime.now().isoformat()))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_account(self, account_number):
        """Retrieve account from database.
        
        Args:
            account_number: Account number to retrieve
            
        Returns:
            dict: Account data or None if not found
        """
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE account_number = ?', (account_number,))
        row = cursor.fetchone()
        if row:
            return {
                'account_number': row[0],
                'pin': row[1],
                'account_holder': row[2],
                'balance': row[3],
                'is_locked': row[4],
                'created_date': row[5],
                'updated_date': row[6]
            }
        return None

    def update_balance(self, account_number, new_balance):
        """Update account balance.
        
        Args:
            account_number: Account to update
            new_balance: New balance amount
            
        Returns:
            bool: True if successful
        """
        cursor = self.connection.cursor()
        cursor.execute(
            'UPDATE accounts SET balance = ?, updated_date = ? WHERE account_number = ?',
            (new_balance, datetime.now().isoformat(), account_number)
        )
        self.connection.commit()
        return True

    def add_transaction(self, transaction_id, account_number, transaction_type, amount, balance_after, description=""):
        """Add transaction to database.
        
        Args:
            transaction_id: Unique transaction ID
            account_number: Associated account
            transaction_type: Type of transaction
            amount: Transaction amount
            balance_after: Balance after transaction
            description: Optional description
            
        Returns:
            bool: True if successful
        """
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO transactions (transaction_id, account_number, transaction_type, amount, balance_after, description, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (transaction_id, account_number, transaction_type, amount, balance_after, description, datetime.now().isoformat()))
        self.connection.commit()
        return True

    def get_transactions(self, account_number, limit=10):
        """Get transaction history for account.
        
        Args:
            account_number: Account to get transactions for
            limit: Number of transactions to retrieve
            
        Returns:
            list: List of transactions
        """
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT * FROM transactions WHERE account_number = ? ORDER BY timestamp DESC LIMIT ?',
            (account_number, limit)
        )
        transactions = []
        for row in cursor.fetchall():
            transactions.append({
                'transaction_id': row[0],
                'account_number': row[1],
                'type': row[2],
                'amount': row[3],
                'balance_after': row[4],
                'description': row[5],
                'timestamp': row[6]
            })
        return transactions

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
