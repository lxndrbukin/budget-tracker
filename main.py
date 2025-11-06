import os
import pandas as pd
from pandas.errors import EmptyDataError
from datetime import datetime
import matplotlib.pyplot as plt
from tabulate import tabulate

class BudgetTracker:
    def __init__(self, columns=["ID","Date","Type","Amount","Category","Description"], file_path=os.path.join(os.path.dirname(__file__), "budget.csv")):
        self.columns = columns
        self.file_path = file_path

    @staticmethod
    def clean_data(data_frame):
        df = data_frame.copy()
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        for c in ["Type","Category","Description"]:
            df[c] = df[c].astype("string").str.strip()
        return df

    @staticmethod
    def create_df(columns):
        return pd.DataFrame(columns=columns)

    def fetch_data(self):
        try:
            raw = pd.read_csv(self.file_path)
            raw = raw.set_index("ID")
        except FileNotFoundError:
            df = self.create_df(self.columns)
            df = df.set_index("ID")
            return df
        return self.clean_data(raw)
    
    def initialize_csv(self):
        if not os.path.exists(self.file_path):
            df = self.create_df(self.columns)
            df.to_csv(self.file_path, index=False)

    def list_transactions(self):
        try:
            df = self.fetch_data()
            if len(df) > 0:
                options = ["All", "By type", "By category"]
                print("List transactions:")
                self.list_options(options)
                choice = int(input("Select an option: "))
                if choice == 1:
                    print(tabulate(df.sort_values("Date").dropna(), headers="keys", tablefmt="pretty"))
                elif choice == 2:
                    self.print_data_by("Type", df)
                elif choice == 3:
                    self.print_data_by("Category", df)
            else:
                raise EmptyDataError("No transactions found!")
        except (FileNotFoundError, EmptyDataError) as e:
            self.print_message(e)

    def add_transaction(self):
        df = self.fetch_data()
        t_types = ["Income", "Expense"]
        self.list_options(t_types)
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
        self.print_message("Transaction added successfully!", 32)
        print(tabulate(new_transaction.set_index("ID"), headers="keys", tablefmt="pretty"))

    def edit_transaction(self):
        try:
            df = self.fetch_data()
            self.list_transactions()
            t_id = int(input("Enter transaction id: "))
            selected_row = df.loc[t_id]
            self.print_message("Selected transaction:", 32)
            print(selected_row)
            columns_list = df.columns.tolist()
            self.print_message(f"Values to update:", 34)
            for i, column in enumerate(columns_list, 1):
                print(f"{i}. {column}")
            option = int(input("Select an option: "))
            new_value = input(f"Enter the new {columns_list[option - 1]} value: ")
            if type(columns_list[option - 1]) is not str:
                df.loc[t_id, columns_list[option - 1]] = float(new_value)
            else:
                df.loc[t_id, columns_list[option - 1]] = new_value
            df.to_csv("budget.csv")
            self.print_message(f"Transaction updated successfully!", 32)
        except FileNotFoundError:
            self.print_message("File does not exist!")
        except ValueError as e:
            self.print_message(e)

    def delete_transaction(self):
        try:
            df = self.fetch_data()
            self.list_transactions()
            t_id = int(input("Enter transaction id: "))
            df = df.drop(t_id)
            df.to_csv("budget.csv")
            self.print_message(f"Transaction under ID {t_id} deleted successfully!", 32)
        except FileNotFoundError:
            self.print_message("File does not exist!")
        except EmptyDataError as e:
            self.print_message(e)

    def print_data_by(self, selection, data_frame):
        if selection not in ("Type", "Category"):
            print("Can only filter by 'Type' or 'Category'.")
            return
        selected = (
            data_frame.assign(Category=lambda d: d[selection])
            .dropna(subset=[selection])
            [selection].drop_duplicates()
            .sort_values()
            .tolist()
        )
        print("Select an option:")
        self.list_options(selected)
        choice = int(input(f"Select a {selection.lower()}: "))
        category = str(selected[choice - 1])
        mask = data_frame[selection].str.casefold() == category.casefold()
        out = data_frame.loc[mask].copy()
        print(out)

    @staticmethod
    def print_message(message, color=31):
        print(f"\033[{color};1m\n{message}\033[0m\n")

    @staticmethod
    def list_options(options):
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

    def is_expense_series(self):
        df = self.fetch_data()
        t = df.get("Type", pd.Series(index=df.index, dtype="string")).astype("string").str.casefold()
        return ~t.eq("income")

    def expense_chart(self):
        df = self.fetch_data()
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

    def summarize(self):
        try:
            df = self.fetch_data()
        except (FileNotFoundError, EmptyDataError):
            print("No transactions yet.")
            raise SystemExit
        by_type = (df.groupby("Type", dropna=True)["Amount"].sum()
                     .sort_values(ascending=False))
        expenses = df.loc[self.is_expense_series()]
        by_cat = (expenses.groupby("Category", dropna=True)["Amount"].sum()
                    .sort_values(ascending=False))
        income_total = by_type.get("Income", 0.0)
        expense_total = expenses["Amount"].sum()
        net = income_total - expense_total
        self.print_message("Totals by Type", 34)
        print(by_type.to_string())
        self.print_message("Totals by Category (expenses)", 34)
        print(by_cat.to_string())
        self.print_message(f"Net: {net:.2f}", 34)
        self.expense_chart()
        self.print_message("Expenses chart saved in your 'charts' folder.",32)

    def run_cli(self):
        self.initialize_csv()
        menu_options = ["Add Transaction", "Delete Transaction", "Edit Transaction", "List Transactions", "Summarize budget", "Exit"]
        while True:
            try:
                self.print_message("Personal Budget Tracker", 34)
                self.list_options(menu_options)
                choice = int(input("Choose an option: "))
                if choice == 1:
                    self.add_transaction()
                elif choice == 2:
                    self.delete_transaction()
                elif choice == 3:
                    self.edit_transaction()
                elif choice == 4:
                    self.list_transactions()
                elif choice == 5:
                    self.summarize()
                elif choice == 6:
                    self.print_message("Program closed.")
                    break
                else:
                    self.print_message("Invalid choice, try again!")
            except KeyboardInterrupt:
                self.print_message("\nProgram stopped by the user.")
                break
            except ValueError:
                self.print_message("Invalid choice, try again!")
            except SystemExit as e:
                self.print_message(e)
                break

if __name__ == "__main__":
    BudgetTracker().run_cli()