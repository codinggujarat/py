import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

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
        self.root.geometry("900x600")

        # Variables
        self.product_id = tk.StringVar()
        self.name = tk.StringVar()
        self.category = tk.StringVar()
        self.price = tk.StringVar()
        self.stock = tk.StringVar()
        self.search = tk.StringVar()
        self.filter_category = tk.StringVar()

        # Product Info Frame
        prod_frame = tk.LabelFrame(self.root, text="Product Information", padx=10, pady=10)
        prod_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(prod_frame, text="Product ID:").grid(row=0, column=0, sticky="w")
        tk.Entry(prod_frame, textvariable=self.product_id).grid(row=0, column=1, padx=5, pady=2)

        tk.Label(prod_frame, text="Product Name:").grid(row=0, column=2, sticky="w")
        tk.Entry(prod_frame, textvariable=self.name).grid(row=0, column=3, padx=5, pady=2)

        tk.Label(prod_frame, text="Category:").grid(row=1, column=0, sticky="w")
        tk.Entry(prod_frame, textvariable=self.category).grid(row=1, column=1, padx=5, pady=2)

        tk.Label(prod_frame, text="Price ($):").grid(row=1, column=2, sticky="w")
        tk.Entry(prod_frame, textvariable=self.price).grid(row=1, column=3, padx=5, pady=2)

        tk.Label(prod_frame, text="Stock Quantity:").grid(row=2, column=0, sticky="w")
        tk.Entry(prod_frame, textvariable=self.stock).grid(row=2, column=1, padx=5, pady=2)

        # Buttons
        btn_frame = tk.Frame(prod_frame)
        btn_frame.grid(row=3, columnspan=4, pady=10)

        tk.Button(btn_frame, text="Add Product", command=self.add_product).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Product", command=self.update_product).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Product", command=self.delete_product).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Update Stock", command=self.update_stock).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Clear Fields", command=self.clear_fields).grid(row=0, column=4, padx=5)

        # Search & Filter Frame
        search_frame = tk.LabelFrame(self.root, text="Search & Filter", padx=10, pady=10)
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky="w")
        tk.Entry(search_frame, textvariable=self.search).grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_product).grid(row=0, column=2, padx=5)

        tk.Label(search_frame, text="Filter by Category:").grid(row=0, column=3, sticky="w")
        self.category_cb = ttk.Combobox(search_frame, textvariable=self.filter_category, values=[], width=15)
        self.category_cb.grid(row=0, column=4, padx=5)

        tk.Button(search_frame, text="Filter", command=self.filter_by_category).grid(row=0, column=5, padx=5)
        tk.Button(search_frame, text="Show All", command=self.show_all).grid(row=0, column=6, padx=5)

        # Inventory Statistics Frame
        stats_frame = tk.LabelFrame(self.root, text="Inventory Statistics", padx=10, pady=10)
        stats_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(stats_frame, text="Low Stock Alert", command=self.low_stock_alert).grid(row=0, column=0, padx=5)
        tk.Button(stats_frame, text="Category Summary", command=self.category_summary).grid(row=0, column=1, padx=5)
        tk.Button(stats_frame, text="Inventory Value", command=self.inventory_value).grid(row=0, column=2, padx=5)

        # Records Frame
        record_frame = tk.LabelFrame(self.root, text="Inventory Records", padx=10, pady=10)
        record_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.txt_records = tk.Text(record_frame, height=15)
        self.txt_records.pack(fill="both", expand=True)
        self.txt_records.insert(tk.END, "No products found. Add some products to get started!")

        connect_db()
        self.show_all()

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
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Product ID already exists!")
        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock quantity!")
        conn.close()

    def update_product(self):
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("""UPDATE products SET name=?, category=?, price=?, stock=? WHERE product_id=?""",
                    (self.name.get(), self.category.get(), float(self.price.get()), int(self.stock.get()), self.product_id.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Product updated successfully!")
        self.show_all()

    def delete_product(self):
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE product_id=?", (self.product_id.get(),))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Product deleted successfully!")
        self.show_all()

    def update_stock(self):
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("UPDATE products SET stock=? WHERE product_id=?",
                    (int(self.stock.get()), self.product_id.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Stock updated successfully!")
        self.show_all()

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
                self.txt_records.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Category: {row[2]} | Price: ${row[3]} | Stock: {row[4]}\n")
        else:
            self.txt_records.insert(tk.END, "No records found.")

    def filter_by_category(self):
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE category=?", (self.filter_category.get(),))
        rows = cur.fetchall()
        conn.close()

        self.txt_records.delete(1.0, tk.END)
        if rows:
            for row in rows:
                self.txt_records.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Category: {row[2]} | Price: ${row[3]} | Stock: {row[4]}\n")
        else:
            self.txt_records.insert(tk.END, "No products found in this category.")

    def show_all(self):
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        conn.close()

        # Update category list in dropdown
        categories = list(set(row[2] for row in rows))
        self.category_cb['values'] = categories

        self.txt_records.delete(1.0, tk.END)
        if rows:
            for row in rows:
                self.txt_records.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Category: {row[2]} | Price: ${row[3]} | Stock: {row[4]}\n")
        else:
            self.txt_records.insert(tk.END, "No products found. Add some products to get started!")

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
            self.txt_records.insert(tk.END, "All products have sufficient stock.")

    def category_summary(self):
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("SELECT category, COUNT(*), SUM(stock) FROM products GROUP BY category")
        rows = cur.fetchall()
        conn.close()

        self.txt_records.delete(1.0, tk.END)
        self.txt_records.insert(tk.END, "📊 Category Summary:\n\n")
        for row in rows:
            self.txt_records.insert(tk.END, f"Category: {row[0]} | Products: {row[1]} | Total Stock: {row[2]}\n")

    def inventory_value(self):
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("SELECT SUM(price * stock) FROM products")
        total_value = cur.fetchone()[0]
        conn.close()

        self.txt_records.delete(1.0, tk.END)
        self.txt_records.insert(tk.END, f"💰 Total Inventory Value: ${total_value if total_value else 0:.2f}")

# ================= Run App =================
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()
