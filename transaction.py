"""Transaction management for ATM simulator."""

from datetime import datetime


class Transaction:
    """Represents a single transaction."""

    TRANSACTION_TYPES = ['WITHDRAWAL', 'DEPOSIT', 'TRANSFER', 'BALANCE_CHECK']

    def __init__(self, account_number, transaction_type, amount, balance_after, description=""):
        """Initialize a transaction.
        
        Args:
            account_number: Account associated with transaction
            transaction_type: Type of transaction
            amount: Transaction amount
            balance_after: Account balance after transaction
            description: Optional transaction description
        """
        self.account_number = account_number
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after
        self.description = description
        self.timestamp = datetime.now()
        self.transaction_id = self._generate_id()

    @staticmethod
    def _generate_id():
        """Generate unique transaction ID.
        
        Returns:
            str: Unique transaction ID
        """
        return f"TXN_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

    def __str__(self):
        """String representation of transaction."""
        return (f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"Type: {self.transaction_type} | "
                f"Amount: ${self.amount:.2f} | "
                f"Balance: ${self.balance_after:.2f}")

    def __repr__(self):
        """Detailed representation of transaction."""
        return (f"Transaction(ID={self.transaction_id}, "
                f"Account={self.account_number}, "
                f"Type={self.transaction_type}, "
                f"Amount=${self.amount:.2f}, "
                f"Time={self.timestamp})")
