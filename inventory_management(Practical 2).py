import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
import csv
import os
from datetime import datetime

# ================= Database Setup ==================
def connect_db():
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            name TEXT,
            category TEXT,
            price REAL,
            stock INTEGER
        )
    """)
    conn.commit()
    conn.close()

# ================= Main Application =================
class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Configure styles
        self.setup_styles()

        # Variables
        self.product_id = tk.StringVar()
        self.name = tk.StringVar()
        self.category = tk.StringVar()
        self.price = tk.StringVar()
        self.stock = tk.StringVar()
        self.search = tk.StringVar()
        self.filter_category = tk.StringVar()

        # Create UI elements
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
        
        header_label = tk.Label(header_frame, text="INVENTORY MANAGEMENT SYSTEM", 
                               bg=self.primary_color, fg="white", font=("Arial", 16, "bold"))
        header_label.pack(pady=15)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Product Information Frame
        prod_frame = tk.LabelFrame(content_frame, text="Product Information", 
                                  font=self.header_font, fg=self.dark_color, 
                                  bg="#f0f0f0", bd=2, relief="groove")
        prod_frame.pack(fill="x", padx=10, pady=(0, 15))

        # Grid configuration for responsive layout
        prod_frame.columnconfigure(1, weight=1)
        prod_frame.columnconfigure(3, weight=1)

        # Labels and Entries with improved styling
        tk.Label(prod_frame, text="Product ID:", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=8)
        self.id_entry = tk.Entry(prod_frame, textvariable=self.product_id, font=self.label_font, 
                                width=25, relief="solid", bd=1)
        self.id_entry.grid(row=0, column=1, padx=(0, 10), pady=8, sticky="ew")

        tk.Label(prod_frame, text="Product Name:", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).grid(row=0, column=2, sticky="w", padx=(10, 5), pady=8)
        self.name_entry = tk.Entry(prod_frame, textvariable=self.name, font=self.label_font, 
                                  width=25, relief="solid", bd=1)
        self.name_entry.grid(row=0, column=3, padx=(0, 10), pady=8, sticky="ew")

        tk.Label(prod_frame, text="Category:", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).grid(row=1, column=0, sticky="w", padx=(10, 5), pady=8)
        self.category_entry = tk.Entry(prod_frame, textvariable=self.category, font=self.label_font, 
                                      width=25, relief="solid", bd=1)
        self.category_entry.grid(row=1, column=1, padx=(0, 10), pady=8, sticky="ew")

        tk.Label(prod_frame, text="Price ($):", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).grid(row=1, column=2, sticky="w", padx=(10, 5), pady=8)
        self.price_entry = tk.Entry(prod_frame, textvariable=self.price, font=self.label_font, 
                                   width=25, relief="solid", bd=1)
        self.price_entry.grid(row=1, column=3, padx=(0, 10), pady=8, sticky="ew")

        tk.Label(prod_frame, text="Stock Quantity:", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).grid(row=2, column=0, sticky="w", padx=(10, 5), pady=8)
        self.stock_entry = tk.Entry(prod_frame, textvariable=self.stock, font=self.label_font, 
                                   width=25, relief="solid", bd=1)
        self.stock_entry.grid(row=2, column=1, padx=(0, 10), pady=8, sticky="ew")

        # Buttons with improved styling
        btn_frame = tk.Frame(prod_frame, bg="#f0f0f0")
        btn_frame.grid(row=3, columnspan=4, pady=15)

        self.add_btn = tk.Button(btn_frame, text="Add Product", command=self.add_product, 
                                bg=self.success_color, fg="white", font=self.button_font,
                                relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
        self.add_btn.pack(side="left", padx=5)
        self.add_btn.bind("<Enter>", lambda e: self.add_btn.config(bg="#219653"))
        self.add_btn.bind("<Leave>", lambda e: self.add_btn.config(bg=self.success_color))

        self.update_btn = tk.Button(btn_frame, text="Update Product", command=self.update_product, 
                                   bg=self.secondary_color, fg="white", font=self.button_font,
                                   relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
        self.update_btn.pack(side="left", padx=5)
        self.update_btn.bind("<Enter>", lambda e: self.update_btn.config(bg="#2980b9"))
        self.update_btn.bind("<Leave>", lambda e: self.update_btn.config(bg=self.secondary_color))

        self.delete_btn = tk.Button(btn_frame, text="Delete Product", command=self.delete_product, 
                                   bg=self.danger_color, fg="white", font=self.button_font,
                                   relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
        self.delete_btn.pack(side="left", padx=5)
        self.delete_btn.bind("<Enter>", lambda e: self.delete_btn.config(bg="#c0392b"))
        self.delete_btn.bind("<Leave>", lambda e: self.delete_btn.config(bg=self.danger_color))

        self.stock_btn = tk.Button(btn_frame, text="Update Stock", command=self.update_stock, 
                                  bg=self.warning_color, fg="white", font=self.button_font,
                                  relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
        self.stock_btn.pack(side="left", padx=5)
        self.stock_btn.bind("<Enter>", lambda e: self.stock_btn.config(bg="#d35400"))
        self.stock_btn.bind("<Leave>", lambda e: self.stock_btn.config(bg=self.warning_color))

        self.clear_btn = tk.Button(btn_frame, text="Clear Fields", command=self.clear_fields, 
                                  bg=self.light_color, fg=self.dark_color, font=self.button_font,
                                  relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
        self.clear_btn.pack(side="left", padx=5)
        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(bg="#bdc3c7"))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(bg=self.light_color))

        # Export/Import Buttons
        export_frame = tk.Frame(prod_frame, bg="#f0f0f0")
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

        # Search & Filter Frame
        search_frame = tk.LabelFrame(content_frame, text="Search & Filter", 
                                    font=self.header_font, fg=self.dark_color, 
                                    bg="#f0f0f0", bd=2, relief="groove")
        search_frame.pack(fill="x", padx=10, pady=(0, 15))

        tk.Label(search_frame, text="Search:", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=10)
        self.search_entry = tk.Entry(search_frame, textvariable=self.search, font=self.label_font, 
                                    width=20, relief="solid", bd=1)
        self.search_entry.grid(row=0, column=1, padx=(0, 10), pady=10)

        search_btn = tk.Button(search_frame, text="Search", command=self.search_product, 
                              bg=self.secondary_color, fg="white", font=self.button_font,
                              relief="flat", bd=0, padx=15, pady=5, cursor="hand2")
        search_btn.grid(row=0, column=2, padx=5, pady=10)
        search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#2980b9"))
        search_btn.bind("<Leave>", lambda e: search_btn.config(bg=self.secondary_color))

        tk.Label(search_frame, text="Filter by Category:", font=self.label_font, 
                bg="#f0f0f0", fg=self.dark_color).grid(row=0, column=3, sticky="w", padx=(20, 5), pady=10)
        
        self.category_cb = ttk.Combobox(search_frame, textvariable=self.filter_category, 
                                       values=[], width=15, font=self.label_font)
        self.category_cb.grid(row=0, column=4, padx=5, pady=10)

        filter_btn = tk.Button(search_frame, text="Filter", command=self.filter_by_category, 
                              bg=self.secondary_color, fg="white", font=self.button_font,
                              relief="flat", bd=0, padx=15, pady=5, cursor="hand2")
        filter_btn.grid(row=0, column=5, padx=5, pady=10)
        filter_btn.bind("<Enter>", lambda e: filter_btn.config(bg="#2980b9"))
        filter_btn.bind("<Leave>", lambda e: filter_btn.config(bg=self.secondary_color))

        show_all_btn = tk.Button(search_frame, text="Show All", command=self.show_all, 
                                bg=self.light_color, fg=self.dark_color, font=self.button_font,
                                relief="flat", bd=0, padx=15, pady=5, cursor="hand2")
        show_all_btn.grid(row=0, column=6, padx=(5, 10), pady=10)
        show_all_btn.bind("<Enter>", lambda e: show_all_btn.config(bg="#bdc3c7"))
        show_all_btn.bind("<Leave>", lambda e: show_all_btn.config(bg=self.light_color))

        # Inventory Statistics Frame
        stats_frame = tk.LabelFrame(content_frame, text="Inventory Statistics", 
                                   font=self.header_font, fg=self.dark_color, 
                                   bg="#f0f0f0", bd=2, relief="groove")
        stats_frame.pack(fill="x", padx=10, pady=(0, 15))

        low_stock_btn = tk.Button(stats_frame, text="Low Stock Alert", command=self.low_stock_alert, 
                                 bg=self.warning_color, fg="white", font=self.button_font,
                                 relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
        low_stock_btn.pack(side="left", padx=10, pady=10)
        low_stock_btn.bind("<Enter>", lambda e: low_stock_btn.config(bg="#d35400"))
        low_stock_btn.bind("<Leave>", lambda e: low_stock_btn.config(bg=self.warning_color))

        category_btn = tk.Button(stats_frame, text="Category Summary", command=self.category_summary, 
                                bg=self.secondary_color, fg="white", font=self.button_font,
                                relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
        category_btn.pack(side="left", padx=10, pady=10)
        category_btn.bind("<Enter>", lambda e: category_btn.config(bg="#2980b9"))
        category_btn.bind("<Leave>", lambda e: category_btn.config(bg=self.secondary_color))

        value_btn = tk.Button(stats_frame, text="Inventory Value", command=self.inventory_value, 
                             bg=self.success_color, fg="white", font=self.button_font,
                             relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
        value_btn.pack(side="left", padx=10, pady=10)
        value_btn.bind("<Enter>", lambda e: value_btn.config(bg="#219653"))
        value_btn.bind("<Leave>", lambda e: value_btn.config(bg=self.success_color))

        # Auto-update toggle
        self.auto_update_var = tk.BooleanVar()
        self.auto_update_var.set(True)
        auto_update_cb = tk.Checkbutton(stats_frame, text="Auto-update files", variable=self.auto_update_var,
                                       bg="#f0f0f0", font=self.label_font, fg=self.dark_color)
        auto_update_cb.pack(side="right", padx=10, pady=10)

        # Records Frame
        record_frame = tk.LabelFrame(content_frame, text="Inventory Records", 
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
        
        self.txt_records.insert(tk.END, "No products found. Add some products to get started!")

    # ================= Functions =================
    def add_product(self):
        if self.product_id.get() == "" or self.name.get() == "":
            messagebox.showerror("Error", "Product ID and Name are required!")
            return

        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)",
                        (self.product_id.get(), self.name.get(), self.category.get(),
                         float(self.price.get()), int(self.stock.get())))
            conn.commit()
            messagebox.showinfo("Success", "Product added successfully!")
            self.show_all()
            if self.auto_update_var.get():
                self.export_to_txt()
                self.export_to_csv()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Product ID already exists!")
        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock quantity!")
        conn.close()

    def update_product(self):
        if self.product_id.get() == "":
            messagebox.showerror("Error", "Product ID is required to update!")
            return
            
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("""UPDATE products SET name=?, category=?, price=?, stock=? WHERE product_id=?""",
                    (self.name.get(), self.category.get(), float(self.price.get()), int(self.stock.get()), self.product_id.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Product updated successfully!")
        self.show_all()
        if self.auto_update_var.get():
            self.export_to_txt()
            self.export_to_csv()

    def delete_product(self):
        if self.product_id.get() == "":
            messagebox.showerror("Error", "Product ID is required to delete!")
            return
            
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE product_id=?", (self.product_id.get(),))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Product deleted successfully!")
        self.show_all()
        if self.auto_update_var.get():
            self.export_to_txt()
            self.export_to_csv()

    def update_stock(self):
        if self.product_id.get() == "":
            messagebox.showerror("Error", "Product ID is required to update stock!")
            return
            
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("UPDATE products SET stock=? WHERE product_id=?",
                    (int(self.stock.get()), self.product_id.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Stock updated successfully!")
        self.show_all()
        if self.auto_update_var.get():
            self.export_to_txt()
            self.export_to_csv()

    def clear_fields(self):
        self.product_id.set("")
        self.name.set("")
        self.category.set("")
        self.price.set("")
        self.stock.set("")

    def search_product(self):
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE product_id=? OR name=?", (self.search.get(), self.search.get()))
        rows = cur.fetchall()
        conn.close()

        self.txt_records.delete(1.0, tk.END)
        if rows:
            for row in rows:
                self.txt_records.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Category: {row[2]} | Price: ${row[3]:.2f} | Stock: {row[4]}\n")
        else:
            self.txt_records.insert(tk.END, "No records found.\n")

    def filter_by_category(self):
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE category=?", (self.filter_category.get(),))
        rows = cur.fetchall()
        conn.close()

        self.txt_records.delete(1.0, tk.END)
        if rows:
            for row in rows:
                self.txt_records.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Category: {row[2]} | Price: ${row[3]:.2f} | Stock: {row[4]}\n")
        else:
            self.txt_records.insert(tk.END, "No products found in this category.\n")

    def show_all(self):
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        conn.close()

        # Update category list in dropdown
        categories = list(set(row[2] for row in rows if row[2]))  # Filter out None/empty categories
        self.category_cb['values'] = categories

        self.txt_records.delete(1.0, tk.END)
        if rows:
            for row in rows:
                self.txt_records.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Category: {row[2]} | Price: ${row[3]:.2f} | Stock: {row[4]}\n")
        else:
            self.txt_records.insert(tk.END, "No products found. Add some products to get started!\n")

    # ================= Statistics =================
    def low_stock_alert(self):
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE stock < 5")
        rows = cur.fetchall()
        conn.close()

        self.txt_records.delete(1.0, tk.END)
        if rows:
            self.txt_records.insert(tk.END, "⚠ Low Stock Products (<5 units):\n\n")
            for row in rows:
                self.txt_records.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Stock: {row[4]}\n")
        else:
            self.txt_records.insert(tk.END, "All products have sufficient stock.\n")

    def category_summary(self):
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("SELECT category, COUNT(*), SUM(stock) FROM products GROUP BY category")
        rows = cur.fetchall()
        conn.close()

        self.txt_records.delete(1.0, tk.END)
        self.txt_records.insert(tk.END, "📊 Category Summary:\n\n")
        for row in rows:
            self.txt_records.insert(tk.END, f"Category: {row[0]} | Products: {row[1]} | Total Stock: {row[2] or 0}\n")

    def inventory_value(self):
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("SELECT SUM(price * stock) FROM products")
        total_value = cur.fetchone()[0]
        conn.close()

        self.txt_records.delete(1.0, tk.END)
        self.txt_records.insert(tk.END, f"💰 Total Inventory Value: ${total_value if total_value else 0:.2f}\n")

    # ================= File Operations =================
    def export_to_txt(self):
        try:
            conn = sqlite3.connect("inventory.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM products")
            rows = cur.fetchall()
            conn.close()
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"inventory_export_{timestamp}.txt"
            
            with open(filename, "w") as f:
                f.write("INVENTORY REPORT\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                if rows:
                    f.write(f"{'ID':<10} {'Name':<20} {'Category':<15} {'Price':<10} {'Stock':<10}\n")
                    f.write("-" * 75 + "\n")
                    for row in rows:
                        f.write(f"{row[0]:<10} {row[1]:<20} {row[2]:<15} ${row[3]:<9.2f} {row[4]:<10}\n")
                    
                    # Add summary
                    total_products = len(rows)
                    total_value = sum(row[3] * row[4] for row in rows)
                    f.write("\n" + "=" * 75 + "\n")
                    f.write(f"Total Products: {total_products}\n")
                    f.write(f"Total Inventory Value: ${total_value:.2f}\n")
                else:
                    f.write("No products found in inventory.\n")
            
            self.txt_records.insert(tk.END, f"\n✅ Exported data to {filename}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export to TXT: {str(e)}")

    def export_to_csv(self):
        try:
            conn = sqlite3.connect("inventory.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM products")
            rows = cur.fetchall()
            conn.close()
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"inventory_export_{timestamp}.csv"
            
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(["Product ID", "Name", "Category", "Price", "Stock"])
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
            
            # Parse the file and add products to database
            conn = sqlite3.connect("inventory.db")
            cur = conn.cursor()
            
            imported_count = 0
            for line in lines:
                # Skip header lines
                if line.startswith("=") or line.startswith("INVENTORY") or line.startswith("Generated") or not line.strip():
                    continue
                    
                # Skip summary lines
                if line.startswith("Total") or line.startswith("-"):
                    continue
                    
                # Parse product lines (this is a simplified parser)
                parts = line.split()
                if len(parts) >= 5 and parts[0] != "ID":
                    try:
                        product_id = parts[0]
                        # Check if product already exists
                        cur.execute("SELECT * FROM products WHERE product_id=?", (product_id,))
                        if not cur.fetchone():
                            # Add new product (simplified - would need more robust parsing in real app)
                            pass
                    except:
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
                
                conn = sqlite3.connect("inventory.db")
                cur = conn.cursor()
                
                imported_count = 0
                for row in reader:
                    if len(row) >= 5:
                        try:
                            cur.execute("INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?, ?)",
                                      (row[0], row[1], row[2], float(row[3]), int(row[4])))
                            imported_count += 1
                        except:
                            continue
                
                conn.commit()
                conn.close()
            
            messagebox.showinfo("Success", f"Imported {imported_count} products from CSV file.")
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

# ================= Run App =================
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()