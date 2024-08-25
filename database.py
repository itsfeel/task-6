import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('billing_app.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT UNIQUE,
                          price REAL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT UNIQUE)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          customer_id INTEGER,
                          product_id INTEGER,
                          date TEXT,
                          payment_status TEXT,
                          FOREIGN KEY(customer_id) REFERENCES customers(id),
                          FOREIGN KEY(product_id) REFERENCES products(id))''')
        self.conn.commit()

    def add_product(self, name, price):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Product already exists.")

    def add_customer(self, name):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO customers (name) VALUES (?)", (name,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Customer already exists.")

    def get_customers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM customers")
        return [row[0] for row in cursor.fetchall()]

    def get_products(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM products")
        return [row[0] for row in cursor.fetchall()]

    def get_product_price(self, product_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT price FROM products WHERE name = ?", (product_name,))
        return cursor.fetchone()[0]

    def get_customer_id(self, customer_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM customers WHERE name = ?", (customer_name,))
        return cursor.fetchone()[0]

    def get_product_id(self, product_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM products WHERE name = ?", (product_name,))
        return cursor.fetchone()[0]

    def add_transaction(self, customer_id, product_id, date, payment_status):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO transactions (customer_id, product_id, date, payment_status) VALUES (?, ?, ?, ?)",
                       (customer_id, product_id, date, payment_status))
        self.conn.commit()

    def close(self):
        self.conn.close()
