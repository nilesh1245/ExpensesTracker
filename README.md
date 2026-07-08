# 💰 Expense Tracker

A simple desktop Expense Tracker built with Python's Tkinter, featuring both a GUI and a CLI mode. Add, view, update, and delete expenses, and see your running total — all backed by a shared logic module so both interfaces stay in sync.

## Features

- **Add expenses** with title, amount, category, and date
- **View all expenses** in a sortable table (GUI) or list (CLI)
- **Edit** an existing expense by selecting it from the table
- **Delete** expenses with a confirmation prompt
- **Live running total** of all expenses
- Input validation (valid amount, valid `YYYY-MM-DD` date, required fields)
- Clean separation between UI and logic — the same `main.py` logic module powers both the GUI and CLI

## Project Structure

```
expense-tracker/
├── ExpensesTrackerGUI.py   # Tkinter GUI front-end
├── main.py                 # Core expense logic (add/view/update/delete/total) + CLI mode
└── README.md
```

## Requirements

- Python 3.8+
- No external packages — uses only the standard library (`tkinter`, `datetime`)

## Getting Started

Clone the repo:

```bash
git clone https://github.com/<your-username>/expense-tracker.git
cd expense-tracker
```

Run the GUI:

```bash
python ExpensesTrackerGUI.py
```

Or run the original CLI version directly:

```bash
python main.py
```

## How It Works

- `main.py` holds all the core logic (`add_expense`, `view_expenses`, `update_expense`, `delete_expense`, `total_expenses`) and can also run standalone as a menu-driven CLI app.
- `ExpensesTrackerGUI.py` imports `main.py` and calls these functions directly from button clicks and form submissions, so there's no duplicated business logic between the two interfaces.

## Notes

- Expense data is currently stored **in memory only** (a Python list) and resets when the app closes. Persisting to a file or database (e.g. JSON, SQLite) would be a natural next step.
- Expense numbering used internally is 1-based, matching the original CLI menu behavior.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
