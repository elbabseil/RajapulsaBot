from app.database.connection import get_connection


class ProductRepository:


    def create_table(self):

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

            buyer_product_status INTEGER,

            seller_product_status INTEGER,

            description TEXT,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        conn.commit()
        conn.close()



    def save_products(self, products):

        conn = get_connection()

        for p in products:

            conn.execute("""
            INSERT OR REPLACE INTO products
            (
                buyer_sku_code,
                product_name,
                category,
                brand,
                price,
                type,
                seller_name,
                buyer_product_status,
                seller_product_status,
                description
            )

            VALUES (?,?,?,?,?,?,?,?,?,?)

            """,
            (
                p.get("buyer_sku_code"),
                p.get("product_name"),
                p.get("category"),
                p.get("brand"),
                p.get("price", 0),
                p.get("type"),
                p.get("seller_name"),
                p.get("buyer_product_status"),
                p.get("seller_product_status"),
                p.get("desc")
            ))

        conn.commit()
        conn.close()



    def get_all(self):

        conn = get_connection()

        cursor = conn.execute("""
            SELECT *
            FROM products
            ORDER BY brand, price
        """)

        data = [
            dict(row)
            for row in cursor.fetchall()
        ]

        conn.close()

        return data



    def get_prepaid(self):

        conn = get_connection()

        cursor = conn.execute("""
            SELECT *
            FROM products
            WHERE category = 'Pulsa'
               OR category = 'Data'
            ORDER BY brand, price
        """)

        data = [
            dict(row)
            for row in cursor.fetchall()
        ]

        conn.close()

        return data



    def get_pasca(self):

        conn = get_connection()

        cursor = conn.execute("""
            SELECT *
            FROM products
            WHERE category NOT IN ('Pulsa','Data')
            ORDER BY brand, price
        """)

        data = [
            dict(row)
            for row in cursor.fetchall()
        ]

        conn.close()

        return data



product_repository = ProductRepository()