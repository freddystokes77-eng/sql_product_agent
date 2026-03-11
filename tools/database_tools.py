from agents import function_tool
from database.sql_database import Database

# Function tool to search the database for products matching a given theme or asset category
# and return the info on those products as a string
@function_tool
def search_database(product_name: str) -> str:

    db = Database("products.db")

    words = product_name.split()

    query = "SELECT id FROM asset_categories WHERE "
    query += " AND ".join(["name LIKE ?" for _ in words])

    params = [f"%{word}%" for word in words]

    asset_category_id = db.cur.execute(query, params).fetchone()

    if asset_category_id is None:
        return "NO_PRODUCTS_FOUND"
    else:
        products = db.cur.execute('''SELECT id, name, ticker, product_type, replication_type, distribution_type, description FROM products WHERE category_id == ?''', (asset_category_id[0],)).fetchall()
        result = ""
        for i, (id, name, ticker, product_type, replication_type, distribution_type, description) in enumerate(products, start=1):
            result += f"{i}. {name}\n   Ticker: {ticker}\n   Description: {description}\n  Product Type: {product_type}\n   Replication Type: {replication_type}\n   Distribution Type: {distribution_type}\n"
            for i, (region, percentage) in enumerate(db.cur.execute('''SELECT region, percentage FROM regional_weightings WHERE product_id == ?''', (id,)).fetchall(), start=1):
                result += f"   Weighting {i}: {region} - {percentage}%\n"
        db.disconnect()
        return result