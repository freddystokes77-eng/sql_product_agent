import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
    
    def disconnect(self):
        self.conn.commit()
        self.conn.close()


Products = Database('products.db') # Fix NOT NULL constraints by removing
regions = Products.cur.execute('''SELECT region, percentage FROM regional_weightings WHERE product_id = 1''').fetchall()


# Products.cur.execute('''DROP TABLE IF EXISTS issuers''')
# Products.cur.execute('''DROP TABLE IF EXISTS products''')
# Products.cur.execute('''DROP TABLE IF EXISTS regional_weightings''')
# Products.disconnect()

# Products = Database('products.db')
# Products.cur.execute('''CREATE TABLE issuers (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL
# )''')
# Products.cur.execute('''CREATE TABLE products (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     ticker TEXT NOT NULL,
#     name TEXT NOT NULL,
#     issuer_id INTEGER NOT NULL,
#     category_id INTEGER NOT NULL,
#     product_type TEXT,
#     replication_type TEXT,
#     distribution_type TEXT,
#     stock_count INTEGER,
#     ongoing_charge REAL,
#     description TEXT
# )''')
# Products.cur.execute('''CREATE TABLE regional_weightings (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     product_id INTEGER NOT NULL,
#     region TEXT NOT NULL,
#     percentage REAL NOT NULL,
#     FOREIGN KEY (product_id) REFERENCES products(id)
# )''')
# Products.disconnect()