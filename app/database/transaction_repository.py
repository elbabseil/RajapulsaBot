from app.database.connection import get_connection
from datetime import datetime



class TransactionRepository:



    def now(self):

        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )



    # =====================================
    # CREATE TABLE
    # =====================================

    def create_table(self):

        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            trx_id TEXT UNIQUE,

            telegram_id TEXT,

            product_code TEXT,

            product_name TEXT,

            customer_no TEXT,

            price INTEGER,

            payment_method TEXT,

            payment_status TEXT,

            transaction_status TEXT,


            qris_id TEXT,

            qr_string TEXT,

            payment_expired TEXT,


            digiflazz_response TEXT,


            created_at TEXT,

            updated_at TEXT

        )
        """)


        conn.commit()

        conn.close()






    # =====================================
    # CREATE TRANSACTION
    # =====================================

    def create(
        self,
        trx_id,
        telegram_id,
        product_code,
        product_name,
        customer_no,
        price,
        payment_method="QRIS"
    ):


        conn = get_connection()


        conn.execute(
        """

        INSERT INTO transactions

        (

        trx_id,

        telegram_id,

        product_code,

        product_name,

        customer_no,

        price,

        payment_method,


        payment_status,

        transaction_status,


        created_at,

        updated_at

        )


        VALUES (?,?,?,?,?,?,?,?,?,?,?)

        """,

        (

        trx_id,

        str(telegram_id),

        product_code,

        product_name,

        customer_no,

        price,

        payment_method,


        "PENDING",

        "PENDING",


        self.now(),

        self.now()

        ))


        conn.commit()

        conn.close()






    # =====================================
    # GET BY TRANSACTION ID
    # =====================================

    def get_by_trx_id(
        self,
        trx_id
    ):


        conn = get_connection()


        cursor = conn.execute(
        """

        SELECT *

        FROM transactions

        WHERE trx_id=?

        """,
        (
            trx_id,
        ))


        row = cursor.fetchone()


        conn.close()


        return dict(row) if row else None






    # =====================================
    # SAVE QRIS
    # =====================================

    def update_qris(
        self,
        trx_id,
        qris_id,
        qr_string,
        expired=None
    ):


        conn = get_connection()


        conn.execute(
        """

        UPDATE transactions

        SET

        qris_id=?,

        qr_string=?,

        payment_expired=?,

        updated_at=?

        WHERE trx_id=?

        """,

        (

        qris_id,

        qr_string,

        expired,

        self.now(),

        trx_id

        ))



        conn.commit()

        conn.close()





    def save_qris(
        self,
        trx_id,
        qris_id,
        qr_string,
        expired=None
    ):

        self.update_qris(
            trx_id,
            qris_id,
            qr_string,
            expired
        )







    # =====================================
    # PAYMENT QUEUE
    # =====================================

    def get_paid_pending(self):


        conn = get_connection()


        cursor = conn.execute(
        """

        SELECT *

        FROM transactions


        WHERE

        payment_status='PAID'


        AND

        transaction_status='PENDING'


        ORDER BY id ASC


        """
        )


        rows = cursor.fetchall()


        conn.close()


        return [

            dict(row)

            for row in rows

        ]








    # =====================================
    # UPDATE STATUS
    # =====================================

    def update_status(
        self,
        trx_id,
        payment_status=None,
        transaction_status=None,
        response=None
    ):


        conn = get_connection()


        conn.execute(
        """

        UPDATE transactions


        SET


        payment_status=

        COALESCE(?,payment_status),


        transaction_status=

        COALESCE(?,transaction_status),


        digiflazz_response=

        COALESCE(?,digiflazz_response),


        updated_at=?


        WHERE trx_id=?


        """,

        (

        payment_status,

        transaction_status,

        response,

        self.now(),

        trx_id

        ))


        conn.commit()

        conn.close()






    # =====================================
    # MARK PROCESSING
    # =====================================

    def mark_processing(
        self,
        trx_id
    ):


        self.update_status(

            trx_id,

            transaction_status="PROCESSING"

        )






    # =====================================
    # MARK SUCCESS
    # =====================================

    def mark_success(
        self,
        trx_id,
        response=None
    ):


        self.update_status(

            trx_id,

            transaction_status="SUCCESS",

            response=response

        )






    # =====================================
    # MARK FAILED
    # =====================================

    def mark_failed(
        self,
        trx_id,
        response=None
    ):


        self.update_status(

            trx_id,

            transaction_status="FAILED",

            response=response

        )







    # =====================================
    # USER HISTORY
    # =====================================

    def get_user_transactions(
        self,
        telegram_id,
        limit=20
    ):


        conn = get_connection()


        cursor = conn.execute(
        """

        SELECT *

        FROM transactions

        WHERE telegram_id=?


        ORDER BY id DESC

        LIMIT ?

        """,

        (

        str(telegram_id),

        limit

        ))



        rows = cursor.fetchall()


        conn.close()



        return [

            dict(row)

            for row in rows

        ]







    # =====================================
    # DASHBOARD
    # =====================================


    def count_transactions(self):

        conn = get_connection()


        result = conn.execute(
        """
        SELECT COUNT(*) total

        FROM transactions
        """
        ).fetchone()


        conn.close()


        return result["total"]




    def count_pending(self):

        conn = get_connection()


        result = conn.execute(
        """
        SELECT COUNT(*) total

        FROM transactions

        WHERE transaction_status='PENDING'

        """
        ).fetchone()


        conn.close()


        return result["total"]





    def count_success(self):

        conn = get_connection()


        result = conn.execute(
        """
        SELECT COUNT(*) total

        FROM transactions

        WHERE transaction_status='SUCCESS'

        """
        ).fetchone()


        conn.close()


        return result["total"]





    def count_failed(self):

        conn = get_connection()


        result = conn.execute(
        """
        SELECT COUNT(*) total

        FROM transactions

        WHERE transaction_status='FAILED'

        """
        ).fetchone()


        conn.close()


        return result["total"]





    def total_revenue(self):

        conn = get_connection()


        result = conn.execute(
        """
        SELECT SUM(price) total

        FROM transactions

        WHERE transaction_status='SUCCESS'

        """
        ).fetchone()


        conn.close()


        return result["total"] or 0






    def get_latest(
        self,
        limit=10
    ):


        conn = get_connection()


        cursor = conn.execute(
        """

        SELECT *

        FROM transactions

        ORDER BY id DESC

        LIMIT ?

        """,
        (
            limit,
        ))



        rows = cursor.fetchall()


        conn.close()


        return [

            dict(row)

            for row in rows

        ]





transaction_repository = TransactionRepository()

transaction_repository.create_table()