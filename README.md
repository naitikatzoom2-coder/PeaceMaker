# ATM Simulator

A Python-based ATM (Automated Teller Machine) simulator that demonstrates banking operations including account management, balance inquiries, withdrawals, deposits, and more.

## Features

- **Account Management**: Create and manage multiple user accounts
- **Authentication**: PIN-based security for account access
- **Balance Inquiry**: Check account balance
- **Withdraw Funds**: Withdraw cash with validation
- **Deposit Funds**: Deposit cash into account
- **Transaction History**: View recent transactions
- **Currency Handling**: Support for different denominations
- **Security**: PIN verification and account locking after failed attempts

## Project Structure

```
├── main.py              # Main entry point
├── atm.py              # ATM class and operations
├── account.py          # Account class
├── transaction.py      # Transaction logging
├── database.py         # Database operations (SQLite)
├── requirements.txt    # Dependencies
├── tests/              # Unit tests
└── README.md          # This file
```

## Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/naitikatzoom2-coder/PeaceMaker.git
cd PeaceMaker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

Run the ATM simulator:
```bash
python main.py
```

## How to Use

1. **Login**: Enter your account number and PIN
2. **Select Operation**:
   - Check Balance
   - Withdraw Cash
   - Deposit Cash
   - View Transaction History
   - Change PIN
   - Logout

## Demo Accounts

The simulator comes with pre-configured demo accounts:

| Account Number | PIN  | Holder Name  | Balance |
|---|---|---|---|
| 1001 | 1234 | John Doe | $5,000 |
| 1002 | 5678 | Jane Smith | $10,000 |
| 1003 | 9999 | Bob Johnson | $2,500 |

## Architecture

### Class Overview

**ATM**: Main ATM machine interface managing all banking operations
- `login()`: Authenticate user
- `logout()`: End session
- `withdraw()`: Withdraw cash
- `deposit()`: Deposit cash
- `check_balance()`: View balance
- `change_pin()`: Update PIN
- `view_transaction_history()`: View past transactions

**Account**: Represents individual user account
- `verify_pin()`: PIN validation
- `deposit()`: Add funds
- `withdraw()`: Remove funds
- `change_pin()`: Update PIN
- `get_balance()`: Retrieve balance

**Database**: SQLite database management
- `add_account()`: Create new account
- `get_account()`: Retrieve account
- `update_balance()`: Update account balance
- `add_transaction()`: Log transaction
- `get_transactions()`: Retrieve transaction history

**Transaction**: Tracks individual transactions
- Transaction ID generation
- Transaction logging
- Timestamp recording

## Security Features

- PIN-based authentication
- Account locking after 3 failed login attempts
- Transaction logging with timestamps
- Balance validation before withdrawal
- Cash denomination tracking

## Contributing

Feel free to fork and submit pull requests for any improvements.

## License

MIT License
