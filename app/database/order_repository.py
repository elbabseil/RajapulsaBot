from app.database.connection import get_connection



class OrderRepository:


    # =========================
    # CREATE TABLE
    # =========================

    def create_table(self):

        conn = get_connection()


        conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            ref_id TEXT UNIQUE,

            customer_no TEXT,

            buyer_sku_code TEXT,

            product_name TEXT,

            price INTEGER,


            qr_id TEXT,


            payment_status TEXT DEFAULT 'UNPAID',

            status TEXT DEFAULT 'PENDING',

            message TEXT,

            sn TEXT,

            provider_response TEXT,

            retry_count INTEGER DEFAULT 0,

            telegram_id INTEGER,


            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)



        # =========================
        # MIGRATION DATABASE LAMA
        # =========================


        migrations = [

            """
            ALTER TABLE orders
            ADD COLUMN payment_status TEXT DEFAULT 'UNPAID'
            """,


            """
            ALTER TABLE orders
            ADD COLUMN qr_id TEXT
            """

        ]



        for migration in migrations:

            try:

                conn.execute(
                    migration
                )


            except Exception:

                pass



        conn.commit()

        conn.close()





    # =========================
    # SAVE ORDER
    # =========================

    def save_order(
        self,
        ref_id,
        customer_no,
        buyer_sku_code,
        product_name,
        price,
        status,
        message,
        sn=None,
        telegram_id=None
    ):


        conn = get_connection()


        conn.execute(
            """
            INSERT INTO orders
            (

                ref_id,

                customer_no,

                buyer_sku_code,

                product_name,

                price,

                payment_status,

                status,

                message,

                sn,

                telegram_id


            )

            VALUES (?,?,?,?,?,?,?,?,?,?)

            """,

            (

                ref_id,

                customer_no,

                buyer_sku_code,

                product_name,

                price,

                "UNPAID",

                status,

                message,

                sn,

                telegram_id

            )

        )


        conn.commit()

        conn.close()





    # =========================
    # UPDATE STATUS
    # =========================

    def update_status(
        self,
        ref_id,
        status,
        message,
        sn=None,
        provider_response=None
    ):


        conn = get_connection()


        conn.execute(
            """
            UPDATE orders

            SET

                status=?,

                message=?,

                sn=?,

                provider_response=?,

                updated_at=CURRENT_TIMESTAMP


            WHERE ref_id=?

            """,

            (

                status,

                message,

                sn,

                provider_response,

                ref_id

            )

        )


        conn.commit()

        conn.close()





    # =========================
    # UPDATE PAYMENT STATUS
    # =========================

    def update_payment_status(
        self,
        ref_id,
        payment_status
    ):


        conn = get_connection()


        conn.execute(
            """
            UPDATE orders

            SET

                payment_status=?,

                updated_at=CURRENT_TIMESTAMP


            WHERE ref_id=?

            """,

            (

                payment_status,

                ref_id

            )

        )


        conn.commit()

        conn.close()





    # =========================
    # SAVE QRIS ID
    # =========================

    def update_qr_id(
        self,
        ref_id,
        qr_id
    ):


        conn = get_connection()


        conn.execute(
            """
            UPDATE orders

            SET

                qr_id=?,

                updated_at=CURRENT_TIMESTAMP


            WHERE ref_id=?

            """,

            (

                qr_id,

                ref_id

            )

        )


        conn.commit()

        conn.close()





    # =========================
    # GET PENDING PAYMENT
    # =========================

    def get_pending_orders(self):


        conn = get_connection()


        cursor = conn.execute(
            """
            SELECT *

            FROM orders


            WHERE

            status='PENDING'

            AND

            qr_id IS NOT NULL


            ORDER BY id ASC

            """
        )



        rows = cursor.fetchall()


        conn.close()



        return [

            dict(row)

            for row in rows

        ]






    # =========================
    # GET PROCESSING
    # =========================

    def get_processing_orders(self):


        conn = get_connection()


        cursor = conn.execute(
            """
            SELECT *

            FROM orders


            WHERE

            status='PROCESSING'


            ORDER BY id ASC

            """
        )



        rows = cursor.fetchall()


        conn.close()



        return [

            dict(row)

            for row in rows

        ]






    # =========================
    # GET ALL
    # =========================

    def get_all(self):


        conn = get_connection()


        cursor = conn.execute(
            """
            SELECT *

            FROM orders

            ORDER BY id DESC

            """
        )



        rows = cursor.fetchall()


        conn.close()



        return [

            dict(row)

            for row in rows

        ]






    # =========================
    # GET BY REF ID
    # =========================

    def get_by_ref(
        self,
        ref_id
    ):


        conn = get_connection()


        cursor = conn.execute(
            """
            SELECT *

            FROM orders

            WHERE ref_id=?

            """,

            (
                ref_id,
            )

        )


        row = cursor.fetchone()


        conn.close()



        return dict(row) if row else None






    # =========================
    # RETRY
    # =========================

    def increase_retry(
        self,
        ref_id
    ):


        conn = get_connection()


        conn.execute(
            """
            UPDATE orders

            SET

            retry_count = retry_count + 1,

            updated_at=CURRENT_TIMESTAMP


            WHERE ref_id=?

            """,

            (
                ref_id,
            )

        )


        conn.commit()

        conn.close()






    def get_retry_count(
        self,
        ref_id
    ):


        conn = get_connection()


        cursor = conn.execute(
            """
            SELECT retry_count

            FROM orders

            WHERE ref_id=?

            """,

            (
                ref_id,
            )

        )


        row = cursor.fetchone()


        conn.close()



        if row:

            return row["retry_count"]


        return 0





    # =========================
    # COUNT
    # =========================

    def count_orders(self):


        conn = get_connection()


        cursor = conn.execute(
            """
            SELECT COUNT(*) total

            FROM orders

            """
        )


        result = cursor.fetchone()


        conn.close()



        return result["total"]





order_repository = OrderRepository()


order_repository.create_table()