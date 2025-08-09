import pandas as pd
from os import path
from datetime import datetime

def initialize_csv():
    if not path.exists('budget.csv'):
        df = pd.DataFrame(columns=['Date', 'Type', 'Amount', 'Category', 'Description'])
        df.to_csv('budget.csv', index=False)

def add_transaction():
    type_ = input("Enter transaction type (Income or Expense): ")
    amount = float(input("Enter the amount of the transaction: "))
    category = input("Enter the category (e.g. Salary, Entertainment, Freelance, Groceries): ")
    description = input("Enter transaction description (e.g. Monthly paycheck): ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv('budget.csv')
    new_transaction = pd.DataFrame([[date, type_, amount, category, description]], columns=['Date', 'Type', 'Amount', 'Category', 'Description'])
    df = pd.concat([df, new_transaction])
    df.to_csv('budget.csv')

def summarize_budget():
    df = pd.read_csv('budget.csv')
    summary = df.groupby('Category')['Amount'].sum()
    print(summary)

while True:
    initialize_csv()
    try:
        pass
    except ValueError:
        pass