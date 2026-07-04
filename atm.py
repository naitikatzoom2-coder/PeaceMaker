"""ATM Machine simulator."""

from account import Account
from transaction import Transaction
from database import Database


class ATM:
    """ATM Machine interface and operations."""

    # Supported denominations
    DENOMINATIONS = [100, 50, 20, 10, 5, 1]

    def __init__(self, db_name='atm.db'):
        """Initialize ATM machine.
        
        Args:
            db_name: Database filename
        """
        self.db = Database(db_name)
        self.current_account = None
        self.cash_available = {100: 50, 50: 50, 20: 100, 10: 100, 5: 100, 1: 200}

    def create_account(self, account_number, pin, account_holder, initial_balance=0.0):
        """Create a new account.
        
        Args:
            account_number: Unique account number
            pin: 4-digit PIN
            account_holder: Account holder name
            initial_balance: Starting balance
            
        Returns:
            bool: True if account created successfully
        """
        if len(str(pin)) != 4 or not str(pin).isdigit():
            print("ERROR: PIN must be 4 digits")
            return False

        if self.db.add_account(account_number, pin, account_holder, initial_balance):
            print(f"SUCCESS: Account {account_number} created for {account_holder}")
            return True
        else:
            print(f"ERROR: Account {account_number} already exists")
            return False

    def login(self, account_number, pin):
        """Login to an account.
        
        Args:
            account_number: Account number
            pin: PIN for authentication
            
        Returns:
            bool: True if login successful
        """
        account_data = self.db.get_account(account_number)
        
        if not account_data:
            print("ERROR: Account not found")
            return False

        if account_data['is_locked']:
            print("ERROR: Account is locked. Please contact customer service")
            return False

        if str(account_data['pin']) == str(pin):
            self.current_account = Account(
                account_number,
                pin,
                account_data['account_holder'],
                account_data['balance']
            )
            print(f"SUCCESS: Welcome {account_data['account_holder']}")
            return True
        else:
            print("ERROR: Incorrect PIN")
            return False

    def logout(self):
        """Logout from current account."""
        if self.current_account:
            self.db.update_balance(self.current_account.account_number, self.current_account.balance)
            self.current_account = None
            print("SUCCESS: Logged out successfully")
            return True
        return False

    def check_balance(self):
        """Check current account balance.
        
        Returns:
            float: Current balance or None
        """
        if not self.current_account:
            print("ERROR: No account logged in")
            return None
        
        balance = self.current_account.get_balance()
        print(f"Your current balance: ${balance:.2f}")
        return balance

    def withdraw(self, amount):
        """Withdraw cash from account.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            bool: True if withdrawal successful
        """
        if not self.current_account:
            print("ERROR: No account logged in")
            return False

        if amount <= 0:
            print("ERROR: Amount must be positive")
            return False

        if amount > self.current_account.balance:
            print("ERROR: Insufficient balance")
            return False

        if not self._check_cash_availability(amount):
            print("ERROR: ATM does not have sufficient cash available")
            return False

        if self.current_account.withdraw(amount):
            self._dispense_cash(amount)
            self.db.add_transaction(
                Transaction._generate_id(),
                self.current_account.account_number,
                'WITHDRAWAL',
                amount,
                self.current_account.balance,
                f"Withdrawal of ${amount:.2f}"
            )
            print(f"SUCCESS: ${amount:.2f} withdrawn")
            print(f"Remaining balance: ${self.current_account.balance:.2f}")
            return True
        
        return False

    def deposit(self, amount):
        """Deposit cash into account.
        
        Args:
            amount: Amount to deposit
            
        Returns:
            bool: True if deposit successful
        """
        if not self.current_account:
            print("ERROR: No account logged in")
            return False

        if amount <= 0:
            print("ERROR: Amount must be positive")
            return False

        if self.current_account.deposit(amount):
            self._add_cash(amount)
            self.db.add_transaction(
                Transaction._generate_id(),
                self.current_account.account_number,
                'DEPOSIT',
                amount,
                self.current_account.balance,
                f"Deposit of ${amount:.2f}"
            )
            print(f"SUCCESS: ${amount:.2f} deposited")
            print(f"New balance: ${self.current_account.balance:.2f}")
            return True
        
        return False

    def change_pin(self, old_pin, new_pin):
        """Change account PIN.
        
        Args:
            old_pin: Current PIN
            new_pin: New PIN
            
        Returns:
            bool: True if PIN changed successfully
        """
        if not self.current_account:
            print("ERROR: No account logged in")
            return False

        if self.current_account.change_pin(old_pin, new_pin):
            self.db.connection.cursor().execute(
                'UPDATE accounts SET pin = ? WHERE account_number = ?',
                (new_pin, self.current_account.account_number)
            )
            self.db.connection.commit()
            print("SUCCESS: PIN changed successfully")
            return True
        else:
            print("ERROR: Failed to change PIN. Check your old PIN and try again")
            return False

    def view_transaction_history(self, limit=5):
        """View transaction history.
        
        Args:
            limit: Number of transactions to display
            
        Returns:
            list: List of transactions
        """
        if not self.current_account:
            print("ERROR: No account logged in")
            return None

        transactions = self.db.get_transactions(self.current_account.account_number, limit)
        
        if not transactions:
            print("No transactions found")
            return transactions

        print(f"\n--- Transaction History (Last {len(transactions)} transactions) ---")
        for txn in transactions:
            print(f"{txn['timestamp']}: {txn['type']:10} | Amount: ${txn['amount']:>8.2f} | Balance: ${txn['balance_after']:.2f}")
        print("--- End of History ---\n")
        
        return transactions

    def _check_cash_availability(self, amount):
        """Check if ATM has enough cash to dispense.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            bool: True if cash is available
        """
        total_available = sum(denom * count for denom, count in self.cash_available.items())
        return amount <= total_available

    def _dispense_cash(self, amount):
        """Dispense cash from ATM.
        
        Args:
            amount: Amount to dispense
        """
        remaining = amount
        dispensed = {}
        
        for denom in self.DENOMINATIONS:
            notes_needed = remaining // denom
            notes_available = self.cash_available[denom]
            notes_to_dispense = min(notes_needed, notes_available)
            
            if notes_to_dispense > 0:
                dispensed[denom] = notes_to_dispense
                self.cash_available[denom] -= notes_to_dispense
                remaining -= notes_to_dispense * denom
        
        if dispensed:
            print("Dispensing:", ", ".join(f"{count}x${denom}" for denom, count in dispensed.items()))

    def _add_cash(self, amount):
        """Add cash to ATM during deposit.
        
        Args:
            amount: Amount being deposited
        """
        remaining = amount
        
        for denom in sorted(self.DENOMINATIONS, reverse=True):
            notes = remaining // denom
            if notes > 0:
                self.cash_available[denom] += notes
                remaining -= notes * denom

    def get_atm_status(self):
        """Get current ATM status.
        
        Returns:
            dict: ATM status information
        """
        total_cash = sum(denom * count for denom, count in self.cash_available.items())
        return {
            'total_cash': total_cash,
            'denominations': self.cash_available.copy(),
            'current_account': self.current_account.account_number if self.current_account else None
        }
