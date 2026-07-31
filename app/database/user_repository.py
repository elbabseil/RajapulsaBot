from app.database.connection import get_connection


class UserRepository:


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
            telegram_id,
            username,
            full_name
        ))

        conn.commit()

        user = self.get_by_telegram_id(telegram_id)

        conn.close()

        return user



    def get_by_telegram_id(self, telegram_id):

        conn = get_connection()

        cursor = conn.execute("""
        SELECT *
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,))

        row = cursor.fetchone()

        conn.close()

        if row:
            return dict(row)

        return None



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

        WHERE telegram_id = ?

        """,
        (
            amount,
            telegram_id
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
                "success": False,
                "message": "Saldo tidak cukup"
            }


        conn = get_connection()


        conn.execute("""
        UPDATE users

        SET balance = balance - ?

        WHERE telegram_id = ?

        """,
        (
            amount,
            telegram_id
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
            "success": True,
            "user": self.get_by_telegram_id(telegram_id)
        }



user_repository = UserRepository()