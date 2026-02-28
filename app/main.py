from sql_database import Database
import sqlite3


product_db = Database('products.db')
product_db.connect()
product_db.execute_query('''DELETE TABLE products''')
product_db.execute_query('''CREATE TABLE IF NOT EXISTS products (
    name TEXT PRIMARY KEY,
    description TEXT NOT NULL)''')
product_db.execute_query('''INSERT INTO products (name, description) VALUES (?, ?)''', ('Sample Product', 'This is a sample product description.'))
print(product_db.execute_query('''SELECT description FROM products WHERE name = ?''', ('Sample Product',)))
product_db.disconnect()