import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None


product_db = Database('products.db')
product_db.connect()
product_db.execute_query('''CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL)''')
product_db.execute_query('''INSERT INTO products (name, description) VALUES (?, ?)''', ('Sample Product', 'This is a sample product description.'))
print(product_db.execute_query('''SELECT description FROM products WHERE name = ?''', ('Sample Product',)))
product_db.disconnect()
