import pandas as pd
from datetime import datetime

class FinanceTracker:
    def __init__(self):
        self.columns = ["Date", "Type", "Category", "Description", "Amount"]
        try:
            self.df = pd.read_csv("finance_data.csv", parse_dates=["Date"])
            print("Loaded existing finance data.")
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=self.columns)

    def add_entry(self, entry_type, category, description, amount, date=None):
        """Add a new income or expense entry."""
        if entry_type not in ["Income", "Expense"]:
            print("Invalid entry type.")
            return

        # Validate date
        if date is None or date.strip() == "":
            date = datetime.today().strftime('%Y-%m-%d')
        try:
            date = pd.to_datetime(date)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        # Validate amount
        try:
            amount = float(amount)
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return

        entry = pd.DataFrame([{
            "Date": date,
            "Type": entry_type,
            "Category": category,
            "Description": description,
            "Amount": amount
        }])

        # ✅ FIX: Avoid pandas FutureWarning for concat with empty DataFrame
        if self.df.empty:
            self.df = entry
        else:
            self.df = pd.concat([self.df, entry], ignore_index=True)

        print(f"{entry_type} added successfully!")

    def view_balance(self):
        """Display total income, expenses, and balance."""
        income = self.df[self.df['Type'] == "Income"]["Amount"].sum()
        expenses = self.df[self.df['Type'] == "Expense"]["Amount"].sum()
        balance = income - expenses

        print("\n💰 ---- Current Financial Summary ----")
        print(f"Total Income:   ₹{income:,.2f}")
        print(f"Total Expenses: ₹{expenses:,.2f}")
        print(f"Current Balance: ₹{balance:,.2f}")

    def category_summary(self):
        """Show total expenses per category."""
        if self.df.empty:
            print("No data to summarize.")
            return

        expenses = self.df[self.df["Type"] == "Expense"]
        if expenses.empty:
            print("No expenses recorded yet.")
            return

        print("\n📊 ---- Category-wise Expense Summary ----")
        summary = expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        print(summary.to_string(float_format="₹{:.2f}".format))

    def monthly_summary(self):
        """Show income, expenses, and balance by month."""
        if self.df.empty:
            print("No data to summarize.")
            return

        df_copy = self.df.copy()
        df_copy["Month"] = df_copy["Date"].dt.to_period("M")
        summary = df_copy.groupby(["Month", "Type"])["Amount"].sum().unstack(fill_value=0)
        summary["Balance"] = summary.get("Income", 0) - summary.get("Expense", 0)

        print("\n📅 ---- Monthly Summary ----")
        print(summary.to_string(float_format="₹{:.2f}".format))

    def export_to_csv(self):
        """Save data to CSV."""
        self.df.to_csv("finance_data.csv", index=False)
        print("✅ Data exported to finance_data.csv")

    def run(self):
        """Main menu loop."""
        while True:
            print("\n==== Personal Finance Tracker ====")
            print("1. Add Income")
            print("2. Add Expense")
            print("3. View Balance")
            print("4. Category Summary")
            print("5. Monthly Summary")
            print("6. Export to CSV")
            print("7. Exit")

            choice = input("Choose an option: ").strip()

            if choice == '1':
                category = input("Enter income category: ")
                description = input("Enter description: ")
                amount = input("Enter amount: ")
                date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
                self.add_entry("Income", category, description, amount, date)

            elif choice == '2':
                category = input("Enter expense category: ")
                description = input("Enter description: ")
                amount = input("Enter amount: ")
                date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
                self.add_entry("Expense", category, description, amount, date)

            elif choice == '3':
                self.view_balance()

            elif choice == '4':
                self.category_summary()

            elif choice == '5':
                self.monthly_summary()

            elif choice == '6':
                self.export_to_csv()

            elif choice == '7':
                self.export_to_csv()
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    tracker = FinanceTracker()
    tracker.run()
