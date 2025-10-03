import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
import csv
import os
from datetime import datetime

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
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Configure styles
        self.setup_styles()

        # --- Variables ---
        self.emp_id = tk.StringVar()
        self.name = tk.StringVar()
        self.department = tk.StringVar()
        self.email = tk.StringVar()
        self.salary = tk.StringVar()
        self.search = tk.StringVar()

        # --- Create UI elements ---
        self.create_widgets()
        connect_db()
        self.show_all()
        self.setup_auto_save()

    def setup_styles(self):
        # Configure colors
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.success_color = "#27ae60"
        self.warning_color = "#f39c12"
        self.danger_color = "#e74c3c"
        self.light_color = "#ecf0f1"
        self.dark_color = "#34495e"
        
        # Configure fonts
        self.header_font = ("Arial", 12, "bold")
        self.label_font = ("Arial", 10)
        self.button_font = ("Arial", 9, "bold")

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="EMPLOYEE MANAGEMENT SYSTEM", 
                               bg=self.primary_color, fg="white", font=("Arial", 16, "bold"))
        header_label.pack(pady=15)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # --- Employee Information Frame ---
        emp_frame = tk.LabelFrame(content_frame, text="Employee Information", 
                                 font=self.header_font, fg=self.dark_color, 
                                 bg="#f0f0f0", bd=2, relief="groove")
        emp_frame.pack(fill="x", padx=10, pady=(0, 15))

        # Grid configuration for responsive layout
        emp_frame.columnconfigure(1, weight=1)
        emp_frame.columnconfigure(3, weight=1)

        # Labels and Entries with improved styling
        tk.Label(emp_frame, text="Employee ID:", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=8)
        self.id_entry = tk.Entry(emp_frame, textvariable=self.emp_id, font=self.label_font, 
                                width=25, relief="solid", bd=1)
        self.id_entry.grid(row=0, column=1, padx=(0, 10), pady=8, sticky="ew")

        tk.Label(emp_frame, text="Name:", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).grid(row=0, column=2, sticky="w", padx=(10, 5), pady=8)
        self.name_entry = tk.Entry(emp_frame, textvariable=self.name, font=self.label_font, 
                                  width=25, relief="solid", bd=1)
        self.name_entry.grid(row=0, column=3, padx=(0, 10), pady=8, sticky="ew")

        tk.Label(emp_frame, text="Department:", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).grid(row=1, column=0, sticky="w", padx=(10, 5), pady=8)
        self.department_entry = tk.Entry(emp_frame, textvariable=self.department, font=self.label_font, 
                                        width=25, relief="solid", bd=1)
        self.department_entry.grid(row=1, column=1, padx=(0, 10), pady=8, sticky="ew")

        tk.Label(emp_frame, text="Salary:", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).grid(row=1, column=2, sticky="w", padx=(10, 5), pady=8)
        self.salary_entry = tk.Entry(emp_frame, textvariable=self.salary, font=self.label_font, 
                                    width=25, relief="solid", bd=1)
        self.salary_entry.grid(row=1, column=3, padx=(0, 10), pady=8, sticky="ew")

        tk.Label(emp_frame, text="Email:", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).grid(row=2, column=0, sticky="w", padx=(10, 5), pady=8)
        self.email_entry = tk.Entry(emp_frame, textvariable=self.email, font=self.label_font, 
                                   width=40, relief="solid", bd=1)
        self.email_entry.grid(row=2, column=1, columnspan=3, padx=(0, 10), pady=8, sticky="ew")

        # Buttons with improved styling
        btn_frame = tk.Frame(emp_frame, bg="#f0f0f0")
        btn_frame.grid(row=3, columnspan=4, pady=15)

        self.add_btn = tk.Button(btn_frame, text="Add Employee", command=self.add_employee, 
                                bg=self.success_color, fg="white", font=self.button_font,
                                relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
        self.add_btn.pack(side="left", padx=5)
        self.add_btn.bind("<Enter>", lambda e: self.add_btn.config(bg="#219653"))
        self.add_btn.bind("<Leave>", lambda e: self.add_btn.config(bg=self.success_color))

        self.update_btn = tk.Button(btn_frame, text="Update Employee", command=self.update_employee, 
                                   bg=self.secondary_color, fg="white", font=self.button_font,
                                   relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
        self.update_btn.pack(side="left", padx=5)
        self.update_btn.bind("<Enter>", lambda e: self.update_btn.config(bg="#2980b9"))
        self.update_btn.bind("<Leave>", lambda e: self.update_btn.config(bg=self.secondary_color))

        self.delete_btn = tk.Button(btn_frame, text="Delete Employee", command=self.delete_employee, 
                                   bg=self.danger_color, fg="white", font=self.button_font,
                                   relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
        self.delete_btn.pack(side="left", padx=5)
        self.delete_btn.bind("<Enter>", lambda e: self.delete_btn.config(bg="#c0392b"))
        self.delete_btn.bind("<Leave>", lambda e: self.delete_btn.config(bg=self.danger_color))

        self.clear_btn = tk.Button(btn_frame, text="Clear Fields", command=self.clear_fields, 
                                  bg=self.light_color, fg=self.dark_color, font=self.button_font,
                                  relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
        self.clear_btn.pack(side="left", padx=5)
        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(bg="#bdc3c7"))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(bg=self.light_color))

        # Export/Import Buttons
        export_frame = tk.Frame(emp_frame, bg="#f0f0f0")
        export_frame.grid(row=4, columnspan=4, pady=5)
        
        tk.Label(export_frame, text="File Operations:", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).pack(side="left", padx=(0, 10))
        
        self.export_txt_btn = tk.Button(export_frame, text="Export to TXT", command=self.export_to_txt, 
                                       bg=self.secondary_color, fg="white", font=self.button_font,
                                       relief="flat", bd=0, padx=15, pady=5, cursor="hand2")
        self.export_txt_btn.pack(side="left", padx=5)
        self.export_txt_btn.bind("<Enter>", lambda e: self.export_txt_btn.config(bg="#2980b9"))
        self.export_txt_btn.bind("<Leave>", lambda e: self.export_txt_btn.config(bg=self.secondary_color))

        self.export_csv_btn = tk.Button(export_frame, text="Export to CSV", command=self.export_to_csv, 
                                       bg=self.secondary_color, fg="white", font=self.button_font,
                                       relief="flat", bd=0, padx=15, pady=5, cursor="hand2")
        self.export_csv_btn.pack(side="left", padx=5)
        self.export_csv_btn.bind("<Enter>", lambda e: self.export_csv_btn.config(bg="#2980b9"))
        self.export_csv_btn.bind("<Leave>", lambda e: self.export_csv_btn.config(bg=self.secondary_color))

        self.import_txt_btn = tk.Button(export_frame, text="Import from TXT", command=self.import_from_txt, 
                                       bg=self.light_color, fg=self.dark_color, font=self.button_font,
                                       relief="flat", bd=0, padx=15, pady=5, cursor="hand2")
        self.import_txt_btn.pack(side="left", padx=5)
        self.import_txt_btn.bind("<Enter>", lambda e: self.import_txt_btn.config(bg="#bdc3c7"))
        self.import_txt_btn.bind("<Leave>", lambda e: self.import_txt_btn.config(bg=self.light_color))

        self.import_csv_btn = tk.Button(export_frame, text="Import from CSV", command=self.import_from_csv, 
                                       bg=self.light_color, fg=self.dark_color, font=self.button_font,
                                       relief="flat", bd=0, padx=15, pady=5, cursor="hand2")
        self.import_csv_btn.pack(side="left", padx=5)
        self.import_csv_btn.bind("<Enter>", lambda e: self.import_csv_btn.config(bg="#bdc3c7"))
        self.import_csv_btn.bind("<Leave>", lambda e: self.import_csv_btn.config(bg=self.light_color))

        # --- Search Frame ---
        search_frame = tk.LabelFrame(content_frame, text="Search", 
                                    font=self.header_font, fg=self.dark_color, 
                                    bg="#f0f0f0", bd=2, relief="groove")
        search_frame.pack(fill="x", padx=10, pady=(0, 15))

        tk.Label(search_frame, text="Search:", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=10)
        self.search_entry = tk.Entry(search_frame, textvariable=self.search, font=self.label_font, 
                                    width=20, relief="solid", bd=1)
        self.search_entry.grid(row=0, column=1, padx=(0, 10), pady=10)

        search_btn = tk.Button(search_frame, text="Search", command=self.search_employee, 
                              bg=self.secondary_color, fg="white", font=self.button_font,
                              relief="flat", bd=0, padx=15, pady=5, cursor="hand2")
        search_btn.grid(row=0, column=2, padx=5, pady=10)
        search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#2980b9"))
        search_btn.bind("<Leave>", lambda e: search_btn.config(bg=self.secondary_color))

        show_all_btn = tk.Button(search_frame, text="Show All", command=self.show_all, 
                                bg=self.light_color, fg=self.dark_color, font=self.button_font,
                                relief="flat", bd=0, padx=15, pady=5, cursor="hand2")
        show_all_btn.grid(row=0, column=3, padx=(5, 10), pady=10)
        show_all_btn.bind("<Enter>", lambda e: show_all_btn.config(bg="#bdc3c7"))
        show_all_btn.bind("<Leave>", lambda e: show_all_btn.config(bg=self.light_color))

        # Auto-update toggle
        self.auto_update_var = tk.BooleanVar()
        self.auto_update_var.set(True)
        auto_update_cb = tk.Checkbutton(search_frame, text="Auto-update files", variable=self.auto_update_var,
                                       bg="#f0f0f0", font=self.label_font, fg=self.dark_color)
        auto_update_cb.grid(row=0, column=4, padx=10, pady=10)

        # --- Employee Records ---
        record_frame = tk.LabelFrame(content_frame, text="Employee Records", 
                                    font=self.header_font, fg=self.dark_color, 
                                    bg="#f0f0f0", bd=2, relief="groove")
        record_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Text widget with scrollbar
        text_frame = tk.Frame(record_frame, bg="#f0f0f0")
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.txt_records = tk.Text(text_frame, height=12, font=("Consolas", 10), 
                                  bg="white", fg=self.dark_color, relief="solid", bd=1)
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.txt_records.yview)
        self.txt_records.configure(yscrollcommand=scrollbar.set)
        
        self.txt_records.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.txt_records.insert(tk.END, "No employees found. Add some employees to get started!")

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
                         self.email.get(), float(self.salary.get()) if self.salary.get() else 0.0))
            conn.commit()
            messagebox.showinfo("Success", "Employee added successfully!")
            self.show_all()
            if self.auto_update_var.get():
                self.export_to_txt()
                self.export_to_csv()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Employee ID already exists!")
        except ValueError:
            messagebox.showerror("Error", "Invalid salary value!")
        conn.close()

    def update_employee(self):
        if self.emp_id.get() == "":
            messagebox.showerror("Error", "Employee ID is required to update!")
            return
            
        conn = sqlite3.connect("employees.db")
        cur = conn.cursor()
        cur.execute("""UPDATE employee SET name=?, department=?, email=?, salary=? WHERE emp_id=?""",
                    (self.name.get(), self.department.get(), self.email.get(), 
                     float(self.salary.get()) if self.salary.get() else 0.0, self.emp_id.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Employee updated successfully!")
        self.show_all()
        if self.auto_update_var.get():
            self.export_to_txt()
            self.export_to_csv()

    def delete_employee(self):
        if self.emp_id.get() == "":
            messagebox.showerror("Error", "Employee ID is required to delete!")
            return
            
        conn = sqlite3.connect("employees.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM employee WHERE emp_id=?", (self.emp_id.get(),))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Employee deleted successfully!")
        self.show_all()
        if self.auto_update_var.get():
            self.export_to_txt()
            self.export_to_csv()

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
                self.txt_records.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Dept: {row[2]} | Email: {row[3]} | Salary: ${row[4]:.2f}\n")
        else:
            self.txt_records.insert(tk.END, "No records found.\n")

    def show_all(self):
        conn = sqlite3.connect("employees.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM employee")
        rows = cur.fetchall()
        conn.close()

        self.txt_records.delete(1.0, tk.END)
        if rows:
            for row in rows:
                self.txt_records.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Dept: {row[2]} | Email: {row[3]} | Salary: ${row[4]:.2f}\n")
        else:
            self.txt_records.insert(tk.END, "No employees found. Add some employees to get started!\n")

    # ================== File Operations ==================
    def export_to_txt(self):
        try:
            conn = sqlite3.connect("employees.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            conn.close()
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"employee_export_{timestamp}.txt"
            
            with open(filename, "w") as f:
                f.write("EMPLOYEE REPORT\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                if rows:
                    f.write(f"{'ID':<10} {'Name':<20} {'Department':<15} {'Email':<25} {'Salary':<10}\n")
                    f.write("-" * 85 + "\n")
                    for row in rows:
                        f.write(f"{row[0]:<10} {row[1]:<20} {row[2]:<15} {row[3]:<25} ${row[4]:<9.2f}\n")
                    
                    # Add summary
                    total_employees = len(rows)
                    total_salary = sum(row[4] for row in rows)
                    avg_salary = total_salary / total_employees if total_employees > 0 else 0
                    f.write("\n" + "=" * 85 + "\n")
                    f.write(f"Total Employees: {total_employees}\n")
                    f.write(f"Total Salary: ${total_salary:.2f}\n")
                    f.write(f"Average Salary: ${avg_salary:.2f}\n")
                else:
                    f.write("No employees found.\n")
            
            self.txt_records.insert(tk.END, f"\n✅ Exported data to {filename}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export to TXT: {str(e)}")

    def export_to_csv(self):
        try:
            conn = sqlite3.connect("employees.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            conn.close()
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"employee_export_{timestamp}.csv"
            
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(["Employee ID", "Name", "Department", "Email", "Salary"])
                # Write data
                writer.writerows(rows)
            
            self.txt_records.insert(tk.END, f"✅ Exported data to {filename}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export to CSV: {str(e)}")

    def import_from_txt(self):
        try:
            filename = filedialog.askopenfilename(
                title="Select TXT file",
                filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
            )
            
            if not filename:
                return
                
            with open(filename, "r") as f:
                lines = f.readlines()
            
            # Parse the file and add employees to database
            conn = sqlite3.connect("employees.db")
            cur = conn.cursor()
            
            imported_count = 0
            for line in lines:
                # Skip header lines
                if line.startswith("=") or line.startswith("EMPLOYEE") or line.startswith("Generated") or not line.strip():
                    continue
                    
                # Skip summary lines
                if line.startswith("Total") or line.startswith("-"):
                    continue
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Imported data from TXT file. Please review and adjust as needed.")
            self.show_all()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import from TXT: {str(e)}")

    def import_from_csv(self):
        try:
            filename = filedialog.askopenfilename(
                title="Select CSV file",
                filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
            )
            
            if not filename:
                return
                
            with open(filename, "r") as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                
                conn = sqlite3.connect("employees.db")
                cur = conn.cursor()
                
                imported_count = 0
                for row in reader:
                    if len(row) >= 5:
                        try:
                            cur.execute("INSERT OR IGNORE INTO employee VALUES (?, ?, ?, ?, ?)",
                                      (row[0], row[1], row[2], row[3], float(row[4]) if row[4] else 0.0))
                            imported_count += 1
                        except:
                            continue
                
                conn.commit()
                conn.close()
            
            messagebox.showinfo("Success", f"Imported {imported_count} employees from CSV file.")
            self.show_all()
            if self.auto_update_var.get():
                self.export_to_txt()
                self.export_to_csv()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import from CSV: {str(e)}")

    def setup_auto_save(self):
        # Auto-save every 5 minutes
        self.root.after(300000, self.auto_save_files)

    def auto_save_files(self):
        if self.auto_update_var.get():
            self.export_to_txt()
            self.export_to_csv()
        # Schedule next auto-save
        self.root.after(300000, self.auto_save_files)

# ================== Run Program ==================
if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()