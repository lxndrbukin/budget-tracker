import pandas as pd
from os import path
from datetime import datetime

menu_options = ["Add Transaction", "List Transactions", "Exit"]

def initialize_csv():
    if not path.exists("budget.csv"):
        df = pd.DataFrame(columns=["Date", "Type", "Amount", "Category", "Description"])
        df.to_csv("budget.csv", index=False)


def add_transaction():
    type_ = input("Enter transaction type (Income or Expense): ")
    amount = float(input("Enter the amount of the transaction: "))
    category = input("Enter the category (e.g. Salary, Entertainment, Freelance, Groceries): ")
    description = input("Enter transaction description (e.g. Monthly paycheck): ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_transaction = pd.DataFrame(
        [[date, type_, amount, category, description]],
        columns=["Date", "Type", "Amount", "Category", "Description"]
    )
    new_transaction.to_csv(
        "budget.csv",
        mode="a",
        index=False,
        header=not path.exists("budget.csv") or path.getsize("budget.csv") == 0
    )
    print("Transaction added successfully!")

def list_transactions():
    list_options = ["All", "By category", "By amount"]
    print("List types:")
    for i, option in enumerate(list_options):
        print(f"{i + 1}. {option}")
    choice = int(input("Choose an option: "))
    if choice == 1:
        df = pd.read_csv('budget.csv', parse_dates=['Date'])
        print(df.sort_values("Date").dropna())
    elif choice == 2:
        df = pd.read_csv('budget.csv')
        cats = (
            df.assign(Category=lambda d: d["Category"].astype("string").str.strip())
            .dropna(subset=["Category"])
            ["Category"].drop_duplicates()
            .sort_values()
            .tolist()
        )
        print("Categories:")
        for i, cat in enumerate(cats):
            print(f"{i + 1}. {cat}")
        cat_choice = int(input("Select a category: "))
        category = str(cats[cat_choice - 1])
        mask = df["Category"].str.casefold() == category.casefold()
        out = df.loc[mask].copy()
        print(out)


def summarize_budget():
    df = pd.read_csv("budget.csv")
    summary = df.groupby("Category")["Amount"].sum()
    print(summary)

def main():
    initialize_csv()
    while True:
        try:
            print("\nPersonal Budget Tracker")
            for i, option in enumerate(menu_options):
                print(f"{i + 1}. {option}")
            choice = int(input("Choose an option: "))
            if choice == 1:
                add_transaction()
            elif choice == 2:
                list_transactions()
            elif choice == 3:
                print("Program closed.")
                break
            else:
                print("Invalid choice, try again!")
        except KeyboardInterrupt:
            print("\nProgram stopped by the user.")
            break

if __name__ == "__main__":
    main()