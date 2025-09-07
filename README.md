# Personal Budget Tracker

A Python-based command-line application for managing personal finances by tracking income and expenses, storing transactions in a CSV file, and generating summaries and expense charts.

## Features
- **Add Transactions**: Record income or expense transactions with details like amount, category, and description.
- **Delete Transactions**: Remove transactions by ID.
- **Edit Transactions**: Update specific fields (Date, Type, Amount, Category, Description) of existing transactions.
- **List Transactions**: View all transactions or filter by type (Income/Expense) or category.
- **Summarize Budget**: Display totals by type and category, calculate net balance, and generate an expense chart saved as `charts/expense_chart.png`.
- **Data Persistence**: Stores transactions in `budget.csv` with automatic initialization if the file doesn't exist.
- **Error Handling**: Handles invalid inputs, file errors, and keyboard interrupts with color-coded messages (red for errors, green for success, blue for summaries).
- **Data Cleaning**: Ensures consistent data types and formats when loading transactions.

## Requirements
- Python 3.x
- Required Python packages (install via `pip`):
  ```bash
  pip install pandas matplotlib
  ```
- A terminal that supports ANSI color codes for colored output (most modern terminals support this).

## Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage
- Launch the program with `python main.py`.
- Choose from the menu options (1-6) to:
  - Add a new transaction (income or expense).
  - Delete a transaction by ID.
  - Edit an existing transaction's details.
  - List transactions (all, by type, or by category).
  - Summarize the budget with totals and generate an expense chart.
  - Exit the program.
- Follow the prompts to input data as required.

## Example
### Adding a Transaction
```
Personal Budget Tracker
1. Add Transaction
2. Delete Transaction
3. Edit Transaction
4. List Transactions
5. Summarize budget
6. Exit
Choose an option: 1
1. Income
2. Expense
Select transaction type: 1
Enter the amount of the transaction: 1000
Enter the category (e.g. Salary, Freelance, Gift): Salary
Enter transaction description (e.g. Monthly paycheck, Gift): Paycheck
Transaction added successfully!
```

### Summarizing Budget
```
Personal Budget Tracker
...
Choose an option: 5
Totals by Type
Type
Income     1000.0
Expense     200.0
Totals by Category (expenses)
Category
Groceries    150.0
Entertainment 50.0
Net: 800.00
Expenses chart saved in your 'charts' folder.
```

### Output Files
- **budget.csv**:
  ```csv
  ID,Date,Type,Amount,Category,Description
  1,2025-09-07 09:00:00,Income,1000.0,Salary,Paycheck
  2,2025-09-07 09:01:00,Expense,150.0,Groceries,Food
  ```
- **charts/expense_chart.png**: A bar chart of expenses by description.

## File Structure
- **main.py**: The core script containing all functionality for the budget tracker.
- **budget.csv**: Stores transaction data (auto-created if not present).
- **charts/**: Directory where expense charts are saved as PNG files.

## Error Handling
- **Invalid Inputs**: Non-numeric inputs or invalid choices trigger a red "Invalid choice, try again!" message.
- **File Errors**: Missing or empty `budget.csv` files are handled with appropriate error messages or initialization.
- **Keyboard Interrupt**: Pressing `Ctrl+C` displays "Program stopped by the user." in red and exits gracefully.
- **Data Validation**: The `clean` function ensures proper data types and formats when loading transactions.

## Notes
- The expense chart is saved in a `charts` directory, which is created automatically if it doesn't exist.
- Categories and descriptions are user-defined, with example suggestions provided during input.
- The program assumes positive amounts for transactions; negative amounts can be used for corrections but are not validated
