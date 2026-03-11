import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
    
    def disconnect(self):
        self.conn.commit()
        self.conn.close()


# Products = Database('products.db')

# # Insert category
# Products.cur.execute('''
# INSERT INTO asset_categories (name)
# VALUES ('Copper')
# ''')

# # Insert issuers
# Products.cur.execute('''
# INSERT INTO issuers (name)
# VALUES ('WisdomTree')
# ''')

# Products.cur.execute('''
# INSERT INTO issuers (name)
# VALUES ('Global X')
# ''')

# # Insert WisdomTree Copper ETC (USD)
# Products.cur.execute('''
# INSERT INTO products
# (ticker, name, issuer_id, category_id, product_type, replication_type, description)
# VALUES
# ('COPA',
#  'WisdomTree Copper',
#  1,
#  1,
#  'ETC',
#  'Futures',
#  'WisdomTree Copper is a fully collateralised, UCITS eligible Exchange Traded Commodity (ETC) designed to provide investors with a total return exposure to Copper futures contracts.')
# ''')

# # Insert WisdomTree Copper ETC (GBP)
# Products.cur.execute('''
# INSERT INTO products
# (ticker, name, issuer_id, category_id, product_type, replication_type, description)
# VALUES
# ('COPB',
#  'WisdomTree Copper',
#  1,
#  1,
#  'ETC',
#  'Futures',
#  'WisdomTree Copper is a fully collateralised, UCITS eligible Exchange Traded Commodity (ETC) designed to provide investors with a total return exposure to Copper futures contracts.')
# ''')

# # Insert Global X Copper Miners ETF
# Products.cur.execute('''
# INSERT INTO products
# (ticker, name, issuer_id, category_id, product_type, ongoing_charge, description)
# VALUES
# ('COPX',
#  'Global X Copper Miners UCITS ETF',
#  2,
#  1,
#  'ETF',
#  0.55,
#  'The Global X Copper Miners UCITS ETF (COPX LN) provides investors access to a broad range of copper mining companies.')
# ''')

# # Save changes
# Products.disconnect()

# Products.cur.execute('''DROP TABLE IF EXISTS asset_categories''')
# Products.cur.execute('''DROP TABLE IF EXISTS issuers''')
# Products.cur.execute('''DROP TABLE IF EXISTS products''')
# Products.cur.execute('''DROP TABLE IF EXISTS regional_weightings''')
# Products.disconnect()

# Products = Database('products.db')
# Products.cur.execute('''CREATE TABLE asset_categories (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL UNIQUE
# )''')
# Products.cur.execute('''CREATE TABLE issuers (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL UNIQUE
# )''')
# Products.cur.execute('''CREATE TABLE products (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     ticker TEXT NOT NULL UNIQUE,
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