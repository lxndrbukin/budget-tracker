import os
import pandas as pd
from pandas.errors import EmptyDataError
from datetime import datetime
import matplotlib.pyplot as plt

def print_message(message, color=31):
    print(f"\033[{color};1m\n{message}\033[0m\n")

def list_options(options):
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

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
        raw = raw.set_index("ID")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ID","Date","Type","Amount","Category","Description"])
        df = df.set_index("ID")
        return df
    return clean(raw)

def initialize_csv():
    if not os.path.exists("budget.csv"):
        df = pd.DataFrame(columns=["ID", "Date", "Type", "Amount", "Category", "Description"])
        df.to_csv("budget.csv", index=False)

def add_transaction():
    df = load_budget()
    t_types = ["Income", "Expense"]
    list_options(t_types)
    t_type = int(input("Select transaction type: "))
    amount = float(input("Enter the amount of the transaction: "))
    category_eg = {
        "income": "Salary, Freelance, Gift",
        "expense": "Entertainment, Groceries, Subscription"
    }
    category = input(f"Enter the category (e.g. {category_eg[t_types[t_type - 1].lower()]}): ")
    desc_eg = {
        "income": "Monthly paycheck, Gift",
        "expense": "Food, ChatGPT, TV"
    }
    description = input(f"Enter transaction description (e.g. {desc_eg[t_types[t_type - 1].lower()]}): ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    t_id =  len(df) + 1
    new_transaction = pd.DataFrame(
        [[t_id, date, t_types[t_type - 1], amount, category, description]],
        columns=["ID", "Date", "Type", "Amount", "Category", "Description"]
    )
    new_transaction.to_csv(
        "budget.csv",
        mode="a",
        index=False,
        header=not os.path.exists("budget.csv") or os.path.getsize("budget.csv") == 0
    )
    print_message("Transaction added successfully!", 32)

def delete_transaction():
    try:
        df = load_budget()
        list_all_transactions()
        t_id = int(input("Enter transaction id: "))
        df = df.drop(t_id)
        df.to_csv("budget.csv")
        print_message(f"Transaction under ID {t_id} deleted successfully!", 32)
    except FileNotFoundError:
        print_message("File does not exist!")
    except EmptyDataError as e:
        print_message(e)

def edit_transaction():
    try:
        df = load_budget()
        list_all_transactions()
        t_id = int(input("Enter transaction id: "))
        selected_row = df.loc[t_id]
        print_message("Selected transaction:", 32)
        print(selected_row)
        columns_list = df.columns.tolist()
        print_message(f"Values to update:", 34)
        for i, column in enumerate(columns_list, 1):
            print(f"{i}. {column}")
        option = int(input("Select an option: "))
        new_value = input(f"Enter the new {columns_list[option - 1]} value: ")
        df.loc[t_id, columns_list[option - 1]] = new_value
        df.to_csv("budget.csv")
        print_message(f"Transaction updated successfully!", 32)
    except FileNotFoundError:
        print_message("File does not exist!")
    except ValueError as e:
        print_message(e)

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
    list_options(selected)
    choice = int(input(f"Select a {selection.lower()}: "))
    category = str(selected[choice - 1])
    mask = data_frame[selection].str.casefold() == category.casefold()
    out = data_frame.loc[mask].copy()
    print(out)

def list_all_transactions():
    try:
        df = load_budget()
        if len(df) > 0:
            print(df.sort_values("Date").dropna())
        else:
            raise EmptyDataError("No transactions found!")
    except (FileNotFoundError, EmptyDataError) as e:
        print_message(e)

def list_transactions():
    try:
        df = load_budget()
        if len(df) > 0:
            options = ["All", "By type", "By category"]
            print("List transactions:")
            list_options(options)
            choice = int(input("Select an option: "))
            if choice == 1:
                list_all_transactions()
            elif choice == 2:
                print_data_by("Type", df)
            elif choice == 3:
                print_data_by("Category", df)
        else:
            raise EmptyDataError("No transactions found!")
    except (FileNotFoundError, EmptyDataError) as e:
        print_message(e)

def is_expense_series():
    df = load_budget()
    t = df.get("Type", pd.Series(index=df.index, dtype="string")).astype("string").str.casefold()
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
    if not os.path.exists("charts"):
        os.mkdir("charts")
    plt.savefig("charts/expense_chart.png")

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
    print_message("Totals by Type", 34)
    print(by_type.to_string())
    print_message("Totals by Category (expenses)", 34)
    print(by_cat.to_string())
    print_message(f"Net: {net:.2f}", 34)
    expense_chart()
    print_message("Expenses chart saved in your 'charts' folder.",32)

def main():
    initialize_csv()
    menu_options = ["Add Transaction", "Delete Transaction", "Edit Transaction", "List Transactions", "Summarize budget", "Exit"]
    while True:
        try:
            print_message("Personal Budget Tracker", 34)
            list_options(menu_options)
            choice = int(input("Choose an option: "))
            if choice == 1:
                add_transaction()
            elif choice == 2:
                delete_transaction()
            elif choice == 3:
                edit_transaction()
            elif choice == 4:
                list_transactions()
            elif choice == 4:
                summarize()
            elif choice == 5:
                print_message("Program closed.")
                break
            else:
                print_message("Invalid choice, try again!")
        except KeyboardInterrupt:
            print_message("\nProgram stopped by the user.")
            break
        except ValueError:
            print_message("Invalid choice, try again!")
        except SystemExit as e:
            print_message(e)
            break

if __name__ == "__main__":
    main()