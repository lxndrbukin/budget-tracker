import pandas as pd
from os import path

def initialize_csv():
    if not path.exists('budget.csv'):
        df = pd.DataFrame(columns=['date', 'type', 'amount', 'category', 'description'])
        df.to_csv('budget.csv', index=False)

def add_transaction(date, type_, amount, category, description):
    df = pd.read_csv('budget.csv')
    new_transaction = pd.DataFrame([[date, type_, amount, category, description]], columns=['date', 'type', 'amount', 'category', 'description'])
    df = pd.concat([df, new_transaction])
    df.to_csv('budget.csv')

def summarize_budget():
    df = pd.read_csv('budget.csv')
    summary = df.groupby('category')['amount'].sum()
    print(summary)