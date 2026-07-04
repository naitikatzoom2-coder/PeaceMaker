"""Main entry point for ATM Simulator."""

from atm import ATM


def print_menu():
    """Print the main menu."""
    print("\n" + "="*50)
    print("         WELCOME TO ATM SIMULATOR")
    print("="*50)
    print("1. Login")
    print("2. Create Account")
    print("3. Exit")
    print("="*50)


def print_transaction_menu():
    """Print the transaction menu."""
    print("\n" + "-"*50)
    print("         TRANSACTION MENU")
    print("-"*50)
    print("1. Check Balance")
    print("2. Withdraw Cash")
    print("3. Deposit Cash")
    print("4. Change PIN")
    print("5. View Transaction History")
    print("6. Logout")
    print("-"*50)


def create_account(atm):
    """Handle account creation."""
    print("\n--- CREATE NEW ACCOUNT ---")
    account_number = input("Enter account number: ").strip()
    account_holder = input("Enter account holder name: ").strip()
    
    while True:
        pin = input("Enter 4-digit PIN: ").strip()
        if len(pin) == 4 and pin.isdigit():
            break
        print("ERROR: PIN must be exactly 4 digits")
    
    initial_balance = input("Enter initial balance (optional, press Enter for 0): ").strip()
    if initial_balance:
        try:
            initial_balance = float(initial_balance)
        except ValueError:
            print("ERROR: Invalid amount")
            return
    else:
        initial_balance = 0.0
    
    atm.create_account(account_number, pin, account_holder, initial_balance)


def login_account(atm):
    """Handle account login."""
    print("\n--- LOGIN ---")
    account_number = input("Enter account number: ").strip()
    pin = input("Enter PIN: ").strip()
    
    if atm.login(account_number, pin):
        handle_transactions(atm)
    else:
        print("Login failed. Please try again.")


def handle_transactions(atm):
    """Handle user transactions after login."""
    while True:
        print_transaction_menu()
        choice = input("Select an option (1-6): ").strip()
        
        if choice == '1':
            atm.check_balance()
        
        elif choice == '2':
            try:
                amount = float(input("Enter amount to withdraw: $"))
                atm.withdraw(amount)
            except ValueError:
                print("ERROR: Invalid amount")
        
        elif choice == '3':
            try:
                amount = float(input("Enter amount to deposit: $"))
                atm.deposit(amount)
            except ValueError:
                print("ERROR: Invalid amount")
        
        elif choice == '4':
            old_pin = input("Enter current PIN: ").strip()
            while True:
                new_pin = input("Enter new 4-digit PIN: ").strip()
                if len(new_pin) == 4 and new_pin.isdigit():
                    break
                print("ERROR: PIN must be exactly 4 digits")
            atm.change_pin(old_pin, new_pin)
        
        elif choice == '5':
            atm.view_transaction_history()
        
        elif choice == '6':
            atm.logout()
            break
        
        else:
            print("ERROR: Invalid option. Please try again.")


def main():
    """Main program loop."""
    atm = ATM()
    
    # Create some demo accounts for testing
    print("Initializing ATM with demo accounts...")
    atm.create_account("1001", "1234", "John Doe", 5000.00)
    atm.create_account("1002", "5678", "Jane Smith", 10000.00)
    atm.create_account("1003", "9999", "Bob Johnson", 2500.00)
    
    while True:
        print_menu()
        choice = input("Select an option (1-3): ").strip()
        
        if choice == '1':
            login_account(atm)
        
        elif choice == '2':
            create_account(atm)
        
        elif choice == '3':
            print("Thank you for using ATM Simulator. Goodbye!")
            atm.db.close()
            break
        
        else:
            print("ERROR: Invalid option. Please try again.")


if __name__ == "__main__":
    main()
