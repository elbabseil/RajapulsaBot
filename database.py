import sqlite3

def init_db():
    """Membuat database dan tabel-tabel yang diperlukan jika belum ada."""
    with sqlite3.connect("bot_database.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                trx_id TEXT PRIMARY KEY,
                user_id INTEGER,
                product_name TEXT,
                phone_number TEXT,
                nominal INTEGER,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS balance_mutations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount INTEGER,
                type TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mutations_user_id ON balance_mutations(user_id)")

        conn.commit()

def save_transaction(trx_id, user_id, product_name, phone_number, nominal, status="PENDING"):
    """Menyimpan transaksi baru ke database."""
    with sqlite3.connect("bot_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO transactions (trx_id, user_id, product_name, phone_number, nominal, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (trx_id, user_id, product_name, phone_number, nominal, status))
        conn.commit()

def update_status(trx_id, status):
    """Mengubah status transaksi."""
    with sqlite3.connect("bot_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE transactions SET status = ? WHERE trx_id = ?
        """, (status, trx_id))
        conn.commit()

def get_transaction(trx_id):
    """Mengambil detail transaksi berdasarkan TRX ID."""
    with sqlite3.connect("bot_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, product_name, phone_number, nominal, status, created_at 
            FROM transactions WHERE trx_id = ?
        """, (trx_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                "user_id": row[0],
                "product_name": row[1],
                "phone_number": row[2],
                "nominal": row[3],
                "status": row[4],
                "created_at": row[5]
            }
        return None

def get_user_transactions(user_id, limit=5, offset=0):
    """Mengambil riwayat transaksi terakhir dengan dukungan paginasi."""
    with sqlite3.connect("bot_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT trx_id, product_name, phone_number, nominal, status, created_at 
            FROM transactions 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
        """, (user_id, limit, offset))
        rows = cursor.fetchall()
        
        return [{
            "trx_id": r[0], "product_name": r[1], "phone_number": r[2],
            "nominal": r[3], "status": r[4], "created_at": r[5]
        } for r in rows]