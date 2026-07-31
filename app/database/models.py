from app.database.connection import get_connection


def create_product_table():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            buyer_sku_code TEXT UNIQUE,

            product_name TEXT,

            category TEXT,

            brand TEXT,

            price INTEGER,

            type TEXT,

            seller_name TEXT,

            buyer_product_status BOOLEAN,

            seller_product_status BOOLEAN,

            desc TEXT,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()