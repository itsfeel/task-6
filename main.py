import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import win32api

customers = []
products = []

def load_data():
    """Load customers and products into the Listbox widgets."""
    customer_list.delete(0, tk.END)
    for customer in customers:
        customer_list.insert(tk.END, customer)
    
    product_list.delete(0, tk.END)
    for product in products:
        product_list.insert(tk.END, f"{product[0]} - ${product[1]:.2f}")

def add_product():
    """Add a new product to the products list."""
    name = product_name_entry.get()
    price = product_price_entry.get()
    if name and price:
        if any(p[0] == name for p in products):
            messagebox.showwarning("Duplicate Product", "Product already exists.")
        else:
            products.append((name, float(price)))
            product_name_entry.delete(0, tk.END)
            product_price_entry.delete(0, tk.END)
            load_data()
    else:
        messagebox.showerror("Input Error", "Enter both name and price.")

def add_customer():
    """Add a new customer to the customers list."""
    name = customer_name_entry.get()
    if name:
        if name in customers:
            messagebox.showwarning("Duplicate Customer", "Customer already exists.")
        else:
            customers.append(name)
            customer_name_entry.delete(0, tk.END)
            load_data()
    else:
        messagebox.showerror("Input Error", "Enter a customer name.")

def delete_product():
    """Delete the selected product from the products list."""
    selected_product = product_list.curselection()
    if selected_product:
        product = product_list.get(selected_product[0]).split(' - ')[0]
        global products
        products = [p for p in products if p[0] != product]
        load_data()
    else:
        messagebox.showerror("Error", "Select a product to delete.")

def delete_customer():
    """Delete the selected customer from the customers list."""
    selected_customer = customer_list.curselection()
    if selected_customer:
        name = customer_list.get(selected_customer[0])
        global customers
        customers = [c for c in customers if c != name]
        load_data()
    else:
        messagebox.showerror("Error", "Select a customer to delete.")

def generate_invoice():
    """Generate an invoice for the selected customer and product."""
    if not customers or not products:
        messagebox.showerror("Error", "No customers or products available.")
        return
    
    customer = customers[0]
    product_name, product_price = products[0]
    
    quantity = quantity_entry.get()
    if not quantity:
        messagebox.showerror("Error", "Enter a quantity.")
        return
    
    try:
        quantity = float(quantity)
    except ValueError:
        messagebox.showerror("Error", "Enter a valid quantity.")
        return
    
    total_price = float(product_price) * quantity
    invoice_text = (
        f"Invoice\n\n"
        f"Customer: {customer}\n"
        f"Product: {product_name}\n"
        f"Quantity: {quantity}\n"
        f"Unit Price: ${product_price:.2f}\n"
        f"Total Price: ${total_price:.2f}"
    )
    
    invoice_display.config(state=tk.NORMAL)
    invoice_display.delete(1.0, tk.END)
    invoice_display.insert(tk.END, invoice_text)
    invoice_display.config(state=tk.DISABLED)
    
    save_invoice(invoice_text)

def save_invoice(invoice_text):
    """Save the invoice text to a file and print it."""
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt")],
                                           title="Save Invoice As")
    if file_path:
        with open(file_path, 'w') as file:
            file.write(invoice_text)
        messagebox.showinfo("Saved", f"Invoice saved to {file_path}")
        print_invoice(file_path)

def print_invoice(file_path):
    """Print the saved invoice file."""
    win32api.ShellExecute(0, "print", file_path, None, ".", 0)

def save_data():
    """Save the customers and products data to a JSON file."""
    data = {'customers': customers, 'products': products}
    with open('billing_data.json', 'w') as file:
        json.dump(data, file)
    messagebox.showinfo("Save", "Data saved successfully.")

def load_from_file():
    """Load customers and products data from a JSON file."""
    if os.path.exists('billing_data.json'):
        with open('billing_data.json', 'r') as file:
            data = json.load(file)
            global customers, products
            customers = data['customers']
            products = data['products']
            load_data()
        messagebox.showinfo("Load", "Data loaded successfully.")
    else:
        messagebox.showwarning("Load", "No saved data found.")

root = tk.Tk()
root.title("Billing Application")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Customer Name:").grid(row=0, column=0, padx=5, pady=5)
customer_name_entry = tk.Entry(frame)
customer_name_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame, text="Add Customer", command=add_customer).grid(row=0, column=2, padx=5, pady=5)
tk.Button(frame, text="Delete Customer", command=delete_customer).grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame, text="Product Name:").grid(row=1, column=0, padx=5, pady=5)
product_name_entry = tk.Entry(frame)
product_name_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Label(frame, text="Product Price:").grid(row=2, column=0, padx=5, pady=5)
product_price_entry = tk.Entry(frame)
product_price_entry.grid(row=2, column=1, padx=5, pady=5)
tk.Button(frame, text="Add Product", command=add_product).grid(row=1, column=2, padx=5, pady=5)
tk.Button(frame, text="Delete Product", command=delete_product).grid(row=2, column=2, padx=5, pady=5)

tk.Label(frame, text="Customers:").grid(row=3, column=0, padx=5, pady=5)
customer_list = tk.Listbox(frame, height=5, width=40)
customer_list.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

tk.Label(frame, text="Products:").grid(row=3, column=2, padx=5, pady=5)
product_list = tk.Listbox(frame, height=5, width=40)
product_list.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

tk.Label(frame, text="Quantity:").grid(row=5, column=0, padx=5, pady=5)
quantity_entry = tk.Entry(frame)
quantity_entry.grid(row=5, column=1, padx=5, pady=5)
tk.Button(frame, text="Generate Invoice", command=generate_invoice).grid(row=5, column=2, columnspan=2, pady=10)

tk.Label(frame, text="Invoice Display:").grid(row=6, column=0, padx=5, pady=5, columnspan=4)
invoice_display = tk.Text(frame, height=10, width=80, wrap=tk.WORD, state=tk.DISABLED)
invoice_display.grid(row=7, column=0, columnspan=4, padx=5, pady=5)

tk.Button(frame, text="Save Data", command=save_data).grid(row=8, column=0, columnspan=2, pady=5)
tk.Button(frame, text="Load Data", command=load_from_file).grid(row=8, column=2, columnspan=2, pady=5)

load_from_file()

root.mainloop()
