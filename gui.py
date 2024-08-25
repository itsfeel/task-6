import tkinter as tk
from tkinter import messagebox
from database import Database

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing Software")
        self.db = Database()

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        tk.Label(self.root, text="Product Name:").grid(row=0, column=0, padx=10, pady=5)
        self.product_name_entry = tk.Entry(self.root)
        self.product_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Price:").grid(row=1, column=0, padx=10, pady=5)
        self.price_entry = tk.Entry(self.root)
        self.price_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Add Product", command=self.add_product).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(self.root, text="Customer Name:").grid(row=3, column=0, padx=10, pady=5)
        self.customer_name_entry = tk.Entry(self.root)
        self.customer_name_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Add Customer", command=self.add_customer).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(self.root, text="Select Customer:").grid(row=5, column=0, padx=10, pady=5)
        self.customer_select = tk.StringVar()
        self.customer_menu = tk.OptionMenu(self.root, self.customer_select, [])
        self.customer_menu.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Select Product:").grid(row=6, column=0, padx=10, pady=5)
        self.product_select = tk.StringVar()
        self.product_menu = tk.OptionMenu(self.root, self.product_select, [])
        self.product_menu.grid(row=6, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Generate Invoice", command=self.generate_invoice).grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def load_data(self):
        customers = self.db.get_customers()
        self.customer_select.set(customers[0] if customers else "")
        menu = self.customer_menu['menu']
        menu.delete(0, 'end')
        for customer in customers:
            menu.add_command(label=customer, command=tk._setit(self.customer_select, customer))

        products = self.db.get_products()
        self.product_select.set(products[0] if products else "")
        menu = self.product_menu['menu']
        menu.delete(0, 'end')
        for product in products:
            menu.add_command(label=product, command=tk._setit(self.product_select, product))

    def add_product(self):
        name = self.product_name_entry.get()
        price = self.price_entry.get()
        if name and price:
            try:
                price = float(price)
                self.db.add_product(name, price)
                self.product_name_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
                self.load_data()
            except ValueError as e:
                messagebox.showwarning("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter both product name and price.")

    def add_customer(self):
        name = self.customer_name_entry.get()
        if name:
            try:
                self.db.add_customer(name)
                self.customer_name_entry.delete(0, tk.END)
                self.load_data()
            except ValueError as e:
                messagebox.showwarning("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter a customer name.")

    def generate_invoice(self):
        customer = self.customer_select.get()
        product = self.product_select.get()
        if customer and product:
            try:
                customer_id = self.db.get_customer_id(customer)
                product_id = self.db.get_product_id(product)
                price = self.db.get_product_price(product)
                self.db.add_transaction(customer_id, product_id)
                messagebox.showinfo("Invoice", f"Customer: {customer}\nProduct: {product}\nPrice: ${price:.2f}")
            except Exception as e:
                messagebox.showwarning("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please select both a customer and a product.")

    def close(self):
        self.db.close()
