import pandas as pd
from pandas.errors import EmptyDataError
from os import path
from datetime import datetime
import matplotlib.pyplot as plt

def clean(data_frame):
    df = data_frame.copy()
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    for c in ["Type","Category","Description"]:
        df[c] = df[c].astype("string").str.strip()
    return df

def load_budget():
    try:
        raw = pd.read_csv("budget.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date","Type","Amount","Category","Description"])
        return df
    return clean(raw)

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

def delete_transaction():
    raw = pd.read_csv("budget.csv")
    df = clean(raw)
    try:
        if len(df) > 0:
            transac_id = int(input("Enter transaction id: "))
            df = df.drop(transac_id)
            df.to_csv("budget.csv", index=False)
            print("Transaction deleted successfully!")
        else:
            raise EmptyDataError("No transactions found!")
    except FileNotFoundError:
        print("File does not exist!")
    except EmptyDataError as e:
        print(e)

def print_data_by(selection, data_frame):
    if selection not in ("Type", "Category"):
        print("Can only filter by 'Type' or 'Category'.")
        return
    selected = (
        clean(data_frame).assign(Category=lambda d: d[selection])
        .dropna(subset=[selection])
        [selection].drop_duplicates()
        .sort_values()
        .tolist()
    )
    print("Select an option:")
    for i, sel in enumerate(selected, 1):
        print(f"{i}. {sel}")
    choice = int(input(f"Select a {selection.lower()}: "))
    category = str(selected[choice - 1])
    mask = data_frame[selection].str.casefold() == category.casefold()
    out = data_frame.loc[mask].copy()
    print(out)

def list_transactions():
    try:
        df = load_budget()
    except (FileNotFoundError, EmptyDataError):
        print("No transactions yet.")
        raise SystemExit
    list_options = ["All", "By type", "By category"]
    print("List types:")
    for i, option in enumerate(list_options, 1):
        print(f"{i}. {option}")
    choice = int(input("Choose an option: "))
    if choice == 1:
        print(df.sort_values("Date").dropna())
    elif choice == 2:
        print_data_by("Type", df)
    elif choice == 3:
        print_data_by("Category", df)

def is_expense_series():
    df = load_budget()
    t = df.get("Type", pd.Series(index=df.index, dtype="string")).astype("string").str.casefold()
    print(t)
    return ~t.eq("income")

def expense_chart():
    df = load_budget()
    is_expense = df["Type"].str.casefold().ne("income")
    by_cat = (df.loc[is_expense]
              .groupby("Description")["Amount"]
              .sum()
              .sort_values(ascending=False))
    plt.bar(by_cat.index.tolist(), by_cat.values.tolist())
    plt.title("Expense Chart")
    plt.xlabel("Type")
    plt.ylabel("Amount")
    plt.savefig("expense_chart.png")

def summarize():
    try:
        df = load_budget()
    except (FileNotFoundError, EmptyDataError):
        print("No transactions yet.")
        raise SystemExit
    by_type = (df.groupby("Type", dropna=True)["Amount"].sum()
                 .sort_values(ascending=False))
    expenses = df.loc[is_expense_series()]
    by_cat = (expenses.groupby("Category", dropna=True)["Amount"].sum()
                .sort_values(ascending=False))
    income_total = by_type.get("Income", 0.0)
    expense_total = expenses["Amount"].sum()
    net = income_total - expense_total
    print("\nTotals by Type")
    print(by_type.to_string())
    print("\nTotals by Category (expenses)")
    print(by_cat.to_string())
    print(f"\nNet: {net:.2f}")
    expense_chart()
    print("Expenses chart saved in your folder.")

def main():
    initialize_csv()
    menu_options = ["Add Transaction", "Delete Transaction", "List Transactions", "Summarize budget", "Exit"]
    while True:
        try:
            print("\nPersonal Budget Tracker")
            for i, option in enumerate(menu_options, 1):
                print(f"{i}. {option}")
            choice = int(input("Choose an option: "))
            if choice == 1:
                add_transaction()
            elif choice == 2:
                delete_transaction()
            elif choice == 3:
                list_transactions()
            elif choice == 4:
                summarize()
            elif choice == 5:
                print("Program closed.")
                break
            else:
                print("Invalid choice, try again!")
        except KeyboardInterrupt:
            print("\nProgram stopped by the user.")
            break
        except SystemExit as e:
            print(e)
            break

if __name__ == "__main__":
    main()