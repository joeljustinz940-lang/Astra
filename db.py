import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ---------------- DATABASE ----------------

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL
)
""")

conn.commit()


# ---------------- FUNCTIONS ----------------

def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()

    if date == "" or category == "" or amount == "":
        messagebox.showerror("Error", "Please fill Date, Category and Amount")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return

    cursor.execute("""
    INSERT INTO expenses (date, category, description, amount)
    VALUES (?, ?, ?, ?)
    """, (date, category, description, amount))

    conn.commit()

    clear_entries()
    show_expenses()

    messagebox.showinfo("Success", "Expense added successfully")


def show_expenses():
    for item in table.get_children():
        table.delete(item)

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    for row in rows:
        table.insert("", tk.END, values=row)

    calculate_total()


def delete_expense():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select an expense to delete")
        return

    item = table.item(selected[0])
    expense_id = item["values"][0]

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()

    show_expenses()

    messagebox.showinfo("Success", "Expense deleted")


def clear_entries():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)


def calculate_total():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    result = cursor.fetchone()[0]

    if result is None:
        result = 0

    total_label.config(
        text=f"Total Expense: ₹{result:.2f}"
    )


# ---------------- GUI ----------------

root = tk.Tk()

root.title("Expense Tracker")
root.geometry("850x650")
root.resizable(False, False)


# Title

title_label = tk.Label(
    root,
    text="EXPENSE TRACKER",
    font=("Arial", 25, "bold")
)

title_label.pack(pady=20)


# Input Frame

input_frame = tk.Frame(root)
input_frame.pack()


# Date

tk.Label(
    input_frame,
    text="Date",
    font=("Arial", 12)
).grid(row=0, column=0, padx=10, pady=8)

date_entry = tk.Entry(
    input_frame,
    width=30
)

date_entry.grid(row=0, column=1, padx=10, pady=8)


# Category

tk.Label(
    input_frame,
    text="Category",
    font=("Arial", 12)
).grid(row=1, column=0, padx=10, pady=8)

category_entry = tk.Entry(
    input_frame,
    width=30
)

category_entry.grid(row=1, column=1, padx=10, pady=8)


# Description

tk.Label(
    input_frame,
    text="Description",
    font=("Arial", 12)
).grid(row=2, column=0, padx=10, pady=8)

description_entry = tk.Entry(
    input_frame,
    width=30
)

description_entry.grid(row=2, column=1, padx=10, pady=8)


# Amount

tk.Label(
    input_frame,
    text="Amount",
    font=("Arial", 12)
).grid(row=3, column=0, padx=10, pady=8)

amount_entry = tk.Entry(
    input_frame,
    width=30
)

amount_entry.grid(row=3, column=1, padx=10, pady=8)


# Buttons

button_frame = tk.Frame(root)
button_frame.pack(pady=15)


add_button = tk.Button(
    button_frame,
    text="Add Expense",
    command=add_expense,
    width=15
)

add_button.grid(row=0, column=0, padx=10)


delete_button = tk.Button(
    button_frame,
    text="Delete Expense",
    command=delete_expense,
    width=15
)

delete_button.grid(row=0, column=1, padx=10)


refresh_button = tk.Button(
    button_frame,
    text="Refresh",
    command=show_expenses,
    width=15
)

refresh_button.grid(row=0, column=2, padx=10)


# ---------------- TABLE ----------------

table_frame = tk.Frame(root)
table_frame.pack(pady=10)


columns = (
    "ID",
    "Date",
    "Category",
    "Description",
    "Amount"
)


table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=12
)


for column in columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        width=150
    )


table.column("ID", width=50)
table.column("Amount", width=100)


table.pack()


# Total

total_label = tk.Label(
    root,
    text="Total Expense: ₹0.00",
    font=("Arial", 18, "bold")
)

total_label.pack(pady=20)


# Load existing expenses

show_expenses()


# Start GUI

root.mainloop()


# Close database when program closes

conn.close()