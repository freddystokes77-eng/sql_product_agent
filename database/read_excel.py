import pandas as pd
import numpy as np
import sqlite3

columns = {
    'asset_categories': ['id', 'name'],
    'issuers': ['id', 'name'],
    'products': ['id', 'ticker', 'name', 'issuer_id', 'category_id', 'product_type', 'replication_type', 'distribution_type', 'stock_count', 'ongoing_charge', 'description'],
    'regional_weightings': ['id', 'product_id', 'region', 'percentage']
}

file = 'data.xlsx'
conn = sqlite3.connect('products.db')

def read_excel(file, writer):
    asset_categories = pd.read_excel(file, sheet_name='asset_categories', index_col=0, engine='openpyxl')
    asset_categories = asset_categories.replace(r'^\s*$', np.nan, regex=True)
    update_table(asset_categories, 'asset_categories', writer)

    issuers = pd.read_excel(file, sheet_name='issuers', index_col=0, engine='openpyxl')
    issuers = issuers.replace(r'^\s*$', np.nan, regex=True)
    update_table(issuers, 'issuers', writer)

    products = pd.read_excel(file, sheet_name='products', index_col=0, engine='openpyxl')
    products = products.replace(r'^\s*$', np.nan, regex=True)
    update_table(products, 'products', writer)

    regional_weightings = pd.read_excel(file, sheet_name='regional_weightings', index_col=0, engine='openpyxl')
    regional_weightings = regional_weightings.replace(r'^\s*$', np.nan, regex=True)
    update_table(regional_weightings, 'regional_weightings', writer)


def update_table(df, table_name, writer):
    for index, row in df.iterrows():
        if not pd.isna(index):
            query = f"UPDATE {table_name} SET "
            values = []
            for col in columns[table_name]:
                if col != 'id' and not pd.isna(row[col]):
                    query += f"{col} = ?, "
                    values.append(row[col])
            query = query.rstrip(", ")
            query += f" WHERE id = {index}"
            conn.execute(query, tuple(values))
        else:
            query = f"INSERT INTO {table_name} ({', '.join(columns[table_name][1:])}) VALUES ({', '.join(['?' for _ in columns[table_name][1:]])})"
            values = [row[col] for col in columns[table_name][1:]]
            conn.execute(query, tuple(values))

            id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            df.at[row.name, 'id'] = id
    conn.commit()
    df.to_excel(writer, sheet_name=table_name, index=False)

if __name__ == "__main__":
    with pd.ExcelWriter('data.xlsx', engine='xlsxwriter') as writer:
        read_excel(file, writer)
    writer.save()
