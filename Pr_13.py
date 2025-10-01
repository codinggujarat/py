import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = pd.DataFrame(columns=["Category", "Amount"])

        # Load existing expenses from CSV if it exists
        self.load_expenses()

        # Input fields
        tk.Label(root, text="Category:").grid(row=0, column=0)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=0, column=1)

        tk.Label(root, text="Amount:").grid(row=1, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=1, column=1)

        tk.Button(root, text="Add Expense", command=self.add_expense).grid(row=2, columnspan=2)
        tk.Button(root, text="Show Report", command=self.show_report).grid(row=3, columnspan=2)

    def load_expenses(self):
        if os.path.exists("expenses.csv"):
            self.expenses = pd.read_csv("expenses.csv")

    def save_expenses(self):
        self.expenses.to_csv("expenses.csv", index=False)

    def add_expense(self):
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        if category and amount.isnumeric():
            new_expense = pd.DataFrame({"Category": [category], "Amount": [float(amount)]})
            self.expenses = pd.concat([self.expenses, new_expense], ignore_index=True)
            self.category_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Added {amount} to {category}!")
            self.save_expenses()  # Save expenses to CSV
        else:
            messagebox.showerror("Error", "Invalid input!")

    def show_report(self):
        if self.expenses.empty:
            messagebox.showwarning("Warning", "No expenses to report!")
            return

        report = self.expenses.groupby('Category').sum()
        report.plot(kind='bar')
        plt.title('Expenses by Category')
        plt.ylabel('Total Amount')
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()