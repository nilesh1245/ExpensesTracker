"""
expense_logic.py

Core expense-tracking logic — adapted from the original CLI version.
The functions here keep the SAME structure and behavior as the original
add_expense / view_expenses / update_expense / delete_expenses / total_expenses,
just without input()/print() calls, so any interface (CLI or GUI) can use them.

A GUI (or CLI) imports this module and calls these functions directly,
passing in the values instead of typing them at a prompt.
"""

expenses = []


def add_expense(title, amount, category, date):
    """Add a new expense. Returns the expense dict that was added."""
    expense = {
        "title": title,
        "amount": float(amount),
        "category": category,
        "date": date
    }
    expenses.append(expense)
    return expense


def view_expenses():
    """Return the list of expenses (empty list if there are none)."""
    if not expenses:
        return []
    return expenses


def update_expense(expense_no, title, amount, category, date):
    """
    Update the expense at position expense_no (1-based, same numbering
    as the original CLI menu). Returns (success: bool, message: str).
    """
    if not expenses:
        return False, "The no expenses data"

    index = expense_no - 1
    if index < 0 or index >= len(expenses):
        return False, "Invalid expense number"

    expenses[index] = {
        "title": title,
        "amount": float(amount),
        "category": category,
        "date": date
    }
    return True, "Expense updated successfully!"


def delete_expense(expense_no):
    """
    Delete the expense at position expense_no (1-based).
    Returns (success: bool, message: str).
    """
    if not expenses:
        return False, "The no expenses data"

    index = expense_no - 1
    if index < 0 or index >= len(expenses):
        return False, "Invalid expense number"

    expenses.pop(index)
    return True, "Expense deleted successfully!"


def total_expenses():
    """Return the total of all expense amounts (0 if there are none)."""
    if not expenses:
        return 0
    return sum(expense["amount"] for expense in expenses)


# ---------------------------------------------------------------
# Optional: still runnable as the original CLI if executed directly
# ---------------------------------------------------------------
def _run_cli():
    def _add():
        title = input("Enter the expense title : ")
        amount = input("Enter the expense amount : ")
        category = input("Enter the expense category : ")
        date = input("Enter the expense date (YYYY-MM-DD) : ")
        add_expense(title, amount, category, date)

    def _view():
        data = view_expenses()
        if not data:
            print("The no expenses data")
            return
        for count, exp in enumerate(data, start=1):
            print(f"{count}{exp}")

    def _update():
        no = int(input("Enter the expense number to update : "))
        title = input("Enter the expense title : ")
        amount = input("Enter the expense amount : ")
        category = input("Enter the expense category : ")
        date = input("Enter the expense date (YYYY-MM-DD) : ")
        ok, msg = update_expense(no, title, amount, category, date)
        print(msg)

    def _delete():
        no = int(input("Enter the expense number to delete : "))
        ok, msg = delete_expense(no)
        print(msg)

    def _total():
        print(f"The Total Expenses: {total_expenses()}")

    while True:
        print("Welcome to the Expense Tracker!")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Total Expenses")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")
        if choice == "1":
            _add()
        elif choice == "2":
            _view()
        elif choice == "3":
            _update()
        elif choice == "4":
            _delete()
        elif choice == "5":
            _total()
        elif choice == "6":
            print("Exiting form the Expenser")
            break


if __name__ == "__main__":
    _run_cli()