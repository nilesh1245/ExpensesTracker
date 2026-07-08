import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import main  # <-- your logic module, connected here


class ExpenseTrackerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("820x560")
        self.minsize(720, 480)
        self.configure(bg="#f4f5f7")
        self.selected_row = None  # index selected in the table (0-based)

        self._build_style()
        self._build_layout()
        self._refresh_table()

    # ---------- style ----------
    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TLabel", background="#f4f5f7", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#f4f5f7", font=("Segoe UI", 18, "bold"))
        style.configure("Total.TLabel", background="#f4f5f7", font=("Segoe UI", 13, "bold"), foreground="#1f6f43")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=26,
                         background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    # ---------- layout ----------
    def _build_layout(self):
        header = ttk.Frame(self, padding=(20, 15, 20, 5))
        header.pack(fill="x")
        ttk.Label(header, text="💰 Expense Tracker", style="Header.TLabel").pack(side="left")
        self.total_var = tk.StringVar()
        ttk.Label(header, textvariable=self.total_var, style="Total.TLabel").pack(side="right")

        form = ttk.LabelFrame(self, text="Add / Update Expense", padding=15)
        form.pack(fill="x", padx=20, pady=10)

        self.title_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(form, text="Title").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.title_var, width=22).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Amount").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.amount_var, width=15).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Category").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.category_var, width=22).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Date (YYYY-MM-DD)").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.date_var, width=15).grid(row=1, column=3, padx=5, pady=5)

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=0, column=4, rowspan=2, padx=(20, 0))
        self.add_btn = ttk.Button(btn_frame, text="Add Expense", command=self.on_add)
        self.add_btn.pack(fill="x", pady=2)
        self.update_btn = ttk.Button(btn_frame, text="Save Update", command=self.on_save_update, state="disabled")
        self.update_btn.pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(fill="x", pady=2)

        table_frame = ttk.Frame(self, padding=(20, 5))
        table_frame.pack(fill="both", expand=True)

        columns = ("title", "amount", "category", "date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        for col, label, width in [
            ("title", "Title", 220),
            ("amount", "Amount", 120),
            ("category", "Category", 150),
            ("date", "Date", 120),
        ]:
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        actions = ttk.Frame(self, padding=(20, 10))
        actions.pack(fill="x")
        ttk.Button(actions, text="Edit Selected", command=self.load_selected_for_edit).pack(side="left", padx=5)
        ttk.Button(actions, text="Delete Selected", command=self.on_delete).pack(side="left", padx=5)
        ttk.Button(actions, text="Refresh", command=self._refresh_table).pack(side="left", padx=5)

    # ---------- validation ----------
    def _valid_form(self):
        if not self.title_var.get().strip():
            messagebox.showwarning("Missing info", "Please enter a title.")
            return False
        try:
            float(self.amount_var.get())
        except ValueError:
            messagebox.showwarning("Invalid amount", "Amount must be a number.")
            return False
        if not self.category_var.get().strip():
            messagebox.showwarning("Missing info", "Please enter a category.")
            return False
        try:
            datetime.strptime(self.date_var.get().strip(), "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Invalid date", "Date must be in YYYY-MM-DD format.")
            return False
        return True

    # ---------- actions: these all call into expense_logic.py ----------
    def on_add(self):
        if not self._valid_form():
            return
        main.add_expense(
            self.title_var.get().strip(),
            self.amount_var.get().strip(),
            self.category_var.get().strip(),
            self.date_var.get().strip(),
        )
        self._refresh_table()
        self.clear_form()

    def on_row_select(self, event=None):
        selection = self.tree.selection()
        self.selected_row = self.tree.index(selection[0]) if selection else None

    def load_selected_for_edit(self):
        if self.selected_row is None:
            messagebox.showinfo("No selection", "Select an expense in the table first.")
            return
        expense = main.view_expenses()[self.selected_row]
        self.title_var.set(expense["title"])
        self.amount_var.set(str(expense["amount"]))
        self.category_var.set(expense["category"])
        self.date_var.set(expense["date"])
        self.add_btn.config(state="disabled")
        self.update_btn.config(state="normal")

    def on_save_update(self):
        if self.selected_row is None:
            messagebox.showinfo("No selection", "Select an expense in the table first.")
            return
        if not self._valid_form():
            return
        ok, msg = main.update_expense(
            self.selected_row + 1,  # expense_logic uses 1-based numbering, like the original CLI
            self.title_var.get().strip(),
            self.amount_var.get().strip(),
            self.category_var.get().strip(),
            self.date_var.get().strip(),
        )
        if not ok:
            messagebox.showerror("Update failed", msg)
            return
        self._refresh_table()
        self.clear_form()

    def on_delete(self):
        if self.selected_row is None:
            messagebox.showinfo("No selection", "Select an expense in the table first.")
            return
        if not messagebox.askyesno("Confirm delete", "Delete this expense?"):
            return
        ok, msg = main.delete_expense(self.selected_row + 1)
        if not ok:
            messagebox.showerror("Delete failed", msg)
            return
        self.selected_row = None
        self._refresh_table()
        self.clear_form()

    def clear_form(self):
        self.title_var.set("")
        self.amount_var.set("")
        self.category_var.set("")
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.add_btn.config(state="normal")
        self.update_btn.config(state="disabled")
        self.selected_row = None
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def _refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for expense in main.view_expenses():
            self.tree.insert(
                "", "end",
                values=(expense["title"], f"{expense['amount']:.2f}", expense["category"], expense["date"])
            )
        self.total_var.set(f"Total: {main.total_expenses():.2f}")


if __name__ == "__main__":
    app = ExpenseTrackerGUI()
    app.mainloop()