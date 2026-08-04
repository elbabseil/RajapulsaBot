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

            username TEXT UNIQUE,

            full_name TEXT,

            password_hash TEXT,

            balance INTEGER DEFAULT 0,

            status TEXT DEFAULT 'ACTIVE',

            password_hash TEXT,

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
    # GET USER BY USERNAME
    # =================================

    def get_by_username(
        self,
        username
    ):

        conn = get_connection()


        cursor = conn.execute("""

        SELECT *

        FROM users

        WHERE username=?

        """,
        (
            username,
        ))


        row = cursor.fetchone()


        conn.close()


        return dict(row) if row else None



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
    # CREATE ADMIN
    # =================================

    def create_admin(
        self,
        telegram_id,
        username,
        full_name,
        password_hash
    ):


        conn = get_connection()


        conn.execute("""

        INSERT INTO users

        (
            telegram_id,
            username,
            full_name,
            password_hash,
            role
        )

        VALUES (?,?,?,?,?)

        """,
        (
            str(telegram_id),
            username,
            full_name,
            password_hash,
            "ADMIN"
        ))


        conn.commit()

        conn.close()







    # =================================
    # GET BY TELEGRAM ID
    # =================================

    def get_by_telegram_id(
        self,
        telegram_id
    ):


        conn = get_connection()


        row = conn.execute("""

        SELECT *

        FROM users

        WHERE telegram_id=?

        """,
        (
            str(telegram_id),
        )).fetchone()


        conn.close()


        return dict(row) if row else None






    # =================================
    # GET BY USERNAME
    # UNTUK LOGIN ADMIN
    # =================================

    def get_by_username(
        self,
        username
    ):


        conn = get_connection()


        row = conn.execute("""

        SELECT *

        FROM users

        WHERE username=?

        """,
        (
            username,
        )).fetchone()


        conn.close()


        return dict(row) if row else None






    # =================================
    # GET ALL USERS
    # =================================

    def get_all(self):


        conn = get_connection()


        rows = conn.execute("""

        SELECT *

        FROM users

        ORDER BY id DESC

        """).fetchall()


        conn.close()


        return [
            dict(row)
            for row in rows
        ]







    # =================================
    # COUNT USER
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
    # TOTAL BALANCE
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
    # UPDATE PASSWORD
    # =================================

    def update_password(
        self,
        username,
        password_hash
    ):


        conn = get_connection()


        conn.execute("""

        UPDATE users

        SET password_hash=?

        WHERE username=?

        """,
        (
            password_hash,
            username
        ))


        conn.commit()

        conn.close()







    # =================================
    # UPDATE STATUS
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

    # =================================
    # GET USER BY USERNAME
    # =================================

    def get_by_username(
        self,
        username
    ):

        conn = get_connection()

        cursor = conn.execute(
            """
            SELECT *
            FROM users
            WHERE username=?
            """,
            (
                username,
            )
        )

        row = cursor.fetchone()

        conn.close()

        return dict(row) if row else None



user_repository = UserRepository()