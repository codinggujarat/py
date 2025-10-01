import tkinter as tk
from tkinter import messagebox
import sqlite3

# ================== Database Setup ==================
def connect_db():
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            emp_id TEXT PRIMARY KEY,
            name TEXT,
            department TEXT,
            email TEXT,
            salary REAL
        )
    """)
    conn.commit()
    conn.close()

# ================== Main Application ==================
class EmployeeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("800x500")

        # --- Variables ---
        self.emp_id = tk.StringVar()
        self.name = tk.StringVar()
        self.department = tk.StringVar()
        self.email = tk.StringVar()
        self.salary = tk.StringVar()
        self.search = tk.StringVar()

        # --- Employee Information Frame ---
        emp_frame = tk.LabelFrame(self.root, text="Employee Information", padx=10, pady=10)
        emp_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(emp_frame, text="Employee ID:").grid(row=0, column=0, sticky="w")
        tk.Entry(emp_frame, textvariable=self.emp_id).grid(row=0, column=1, padx=5, pady=2)

        tk.Label(emp_frame, text="Name:").grid(row=0, column=2, sticky="w")
        tk.Entry(emp_frame, textvariable=self.name).grid(row=0, column=3, padx=5, pady=2)

        tk.Label(emp_frame, text="Department:").grid(row=1, column=0, sticky="w")
        tk.Entry(emp_frame, textvariable=self.department).grid(row=1, column=1, padx=5, pady=2)

        tk.Label(emp_frame, text="Salary:").grid(row=1, column=2, sticky="w")
        tk.Entry(emp_frame, textvariable=self.salary).grid(row=1, column=3, padx=5, pady=2)

        tk.Label(emp_frame, text="Email:").grid(row=2, column=0, sticky="w")
        tk.Entry(emp_frame, textvariable=self.email, width=40).grid(row=2, column=1, columnspan=3, padx=5, pady=2)

        # Buttons
        btn_frame = tk.Frame(emp_frame)
        btn_frame.grid(row=3, columnspan=4, pady=10)

        tk.Button(btn_frame, text="Add Employee", command=self.add_employee).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Employee", command=self.update_employee).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Employee", command=self.delete_employee).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Clear Fields", command=self.clear_fields).grid(row=0, column=3, padx=5)

        # --- Search Frame ---
        search_frame = tk.LabelFrame(self.root, text="Search", padx=10, pady=10)
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky="w")
        tk.Entry(search_frame, textvariable=self.search).grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_employee).grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Show All", command=self.show_all).grid(row=0, column=3, padx=5)

        # --- Employee Records ---
        record_frame = tk.LabelFrame(self.root, text="Employee Records", padx=10, pady=10)
        record_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.txt_records = tk.Text(record_frame, height=15)
        self.txt_records.pack(fill="both", expand=True)
        self.txt_records.insert(tk.END, "No employees found. Add some employees to get started!")

        connect_db()
        self.show_all()

    # ================== Functions ==================
    def add_employee(self):
        if self.emp_id.get() == "" or self.name.get() == "":
            messagebox.showerror("Error", "Employee ID and Name are required!")
            return

        conn = sqlite3.connect("employees.db")
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO employee VALUES (?, ?, ?, ?, ?)", 
                        (self.emp_id.get(), self.name.get(), self.department.get(), 
                         self.email.get(), self.salary.get()))
            conn.commit()
            messagebox.showinfo("Success", "Employee added successfully!")
            self.show_all()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Employee ID already exists!")
        conn.close()

    def update_employee(self):
        conn = sqlite3.connect("employees.db")
        cur = conn.cursor()
        cur.execute("""UPDATE employee SET name=?, department=?, email=?, salary=? WHERE emp_id=?""",
                    (self.name.get(), self.department.get(), self.email.get(), self.salary.get(), self.emp_id.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Employee updated successfully!")
        self.show_all()

    def delete_employee(self):
        conn = sqlite3.connect("employees.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM employee WHERE emp_id=?", (self.emp_id.get(),))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Employee deleted successfully!")
        self.show_all()

    def clear_fields(self):
        self.emp_id.set("")
        self.name.set("")
        self.department.set("")
        self.email.set("")
        self.salary.set("")

    def search_employee(self):
        conn = sqlite3.connect("employees.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM employee WHERE emp_id=? OR name=?", 
                    (self.search.get(), self.search.get()))
        rows = cur.fetchall()
        conn.close()

        self.txt_records.delete(1.0, tk.END)
        if rows:
            for row in rows:
                self.txt_records.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Dept: {row[2]} | Email: {row[3]} | Salary: {row[4]}\n")
        else:
            self.txt_records.insert(tk.END, "No records found.")

    def show_all(self):
        conn = sqlite3.connect("employees.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM employee")
        rows = cur.fetchall()
        conn.close()

        self.txt_records.delete(1.0, tk.END)
        if rows:
            for row in rows:
                self.txt_records.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Dept: {row[2]} | Email: {row[3]} | Salary: {row[4]}\n")
        else:
            self.txt_records.insert(tk.END, "No employees found. Add some employees to get started!")

# ================== Run Program ==================
if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()
