from app.database.connection import get_connection



class UserRepository:


    # =================================
    # CREATE TABLE
    # =================================

    def create_table(self):

        conn = get_connection()


        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            telegram_id TEXT UNIQUE,

            username TEXT,

            full_name TEXT,

            balance INTEGER DEFAULT 0,

            status TEXT DEFAULT 'ACTIVE',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)



        conn.execute("""
        CREATE TABLE IF NOT EXISTS balance_mutations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            amount INTEGER,

            type TEXT,

            description TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)



        conn.commit()

        conn.close()





    # =================================
    # CREATE USER
    # =================================

    def create_user(
        self,
        telegram_id,
        username=None,
        full_name=None
    ):


        conn = get_connection()


        conn.execute("""
        INSERT OR IGNORE INTO users

        (
            telegram_id,
            username,
            full_name
        )

        VALUES (?,?,?)

        """,
        (
            str(telegram_id),
            username,
            full_name
        ))


        conn.commit()

        conn.close()


        return self.get_by_telegram_id(
            telegram_id
        )






    # =================================
    # GET USER
    # =================================

    def get_by_telegram_id(
        self,
        telegram_id
    ):


        conn = get_connection()


        cursor = conn.execute("""

        SELECT *

        FROM users

        WHERE telegram_id=?

        """,
        (
            str(telegram_id),
        ))


        row = cursor.fetchone()


        conn.close()


        return dict(row) if row else None





    # =================================
    # GET ALL USERS
    # =================================

    def get_all(self):


        conn = get_connection()


        cursor = conn.execute("""

        SELECT *

        FROM users

        ORDER BY id DESC

        """)


        data = [

            dict(row)

            for row in cursor.fetchall()

        ]


        conn.close()


        return data






    # =================================
    # DASHBOARD
    # TOTAL USER
    # =================================

    def count_users(self):


        conn = get_connection()


        result = conn.execute("""

        SELECT COUNT(*) total

        FROM users

        """).fetchone()


        conn.close()


        return result["total"]






    # =================================
    # DASHBOARD
    # TOTAL SALDO USER
    # =================================

    def total_balance(self):


        conn = get_connection()


        result = conn.execute("""

        SELECT SUM(balance) total

        FROM users

        """).fetchone()


        conn.close()


        return result["total"] or 0





    # =================================
    # USER TERBARU DASHBOARD
    # =================================

    def get_latest_users(
        self,
        limit=10
    ):


        conn = get_connection()


        cursor = conn.execute("""

        SELECT *

        FROM users

        ORDER BY id DESC

        LIMIT ?

        """,
        (
            limit,
        ))


        data = [

            dict(row)

            for row in cursor.fetchall()

        ]


        conn.close()


        return data





    # =================================
    # TAMBAH SALDO
    # =================================

    def add_balance(
        self,
        telegram_id,
        amount,
        description="Topup"
    ):


        user = self.get_by_telegram_id(
            telegram_id
        )


        if not user:

            return None



        conn = get_connection()



        conn.execute("""

        UPDATE users

        SET balance = balance + ?

        WHERE telegram_id=?

        """,
        (
            amount,
            str(telegram_id)
        ))



        conn.execute("""

        INSERT INTO balance_mutations

        (
            user_id,
            amount,
            type,
            description
        )

        VALUES (?,?,?,?)

        """,
        (
            user["id"],
            amount,
            "CREDIT",
            description
        ))



        conn.commit()

        conn.close()



        return self.get_by_telegram_id(
            telegram_id
        )






    # =================================
    # KURANGI SALDO
    # =================================

    def subtract_balance(
        self,
        telegram_id,
        amount,
        description="Pembelian"
    ):


        user = self.get_by_telegram_id(
            telegram_id
        )


        if not user:

            return None



        if user["balance"] < amount:

            return {

                "success":False,

                "message":"Saldo tidak cukup"

            }



        conn = get_connection()



        conn.execute("""

        UPDATE users

        SET balance = balance - ?

        WHERE telegram_id=?

        """,
        (
            amount,
            str(telegram_id)
        ))



        conn.execute("""

        INSERT INTO balance_mutations

        (
            user_id,
            amount,
            type,
            description
        )

        VALUES (?,?,?,?)

        """,
        (
            user["id"],
            -amount,
            "DEBIT",
            description
        ))



        conn.commit()

        conn.close()



        return {

            "success":True,

            "user":
            self.get_by_telegram_id(
                telegram_id
            )

        }





    # =================================
    # HISTORI SALDO
    # =================================

    def get_balance_mutations(
        self,
        user_id,
        limit=20
    ):


        conn = get_connection()


        cursor = conn.execute("""

        SELECT *

        FROM balance_mutations

        WHERE user_id=?

        ORDER BY id DESC

        LIMIT ?

        """,
        (
            user_id,
            limit
        ))



        data = [

            dict(row)

            for row in cursor.fetchall()

        ]



        conn.close()


        return data





    # =================================
    # UPDATE STATUS USER
    # =================================

    def update_status(
        self,
        telegram_id,
        status
    ):


        conn = get_connection()


        conn.execute("""

        UPDATE users

        SET status=?

        WHERE telegram_id=?

        """,
        (
            status,
            str(telegram_id)
        ))


        conn.commit()

        conn.close()





    # =================================
    # DELETE USER
    # =================================

    def delete_user(
        self,
        telegram_id
    ):


        conn = get_connection()


        conn.execute("""

        DELETE FROM users

        WHERE telegram_id=?

        """,
        (
            str(telegram_id),
        ))


        conn.commit()

        conn.close()





user_repository = UserRepository()