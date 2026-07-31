import sqlite3
from pathlib import Path

# Folder penyimpanan database
BASE_DIR = Path(__file__).resolve().parents[2]
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)

DB_PATH = STORAGE_DIR / "bot_database.db"


def get_connection():
    """
    Membuat koneksi SQLite.
    Seluruh aplikasi (Bot, API, Dashboard, Worker)
    menggunakan fungsi ini.
    """

    conn = sqlite3.connect(DB_PATH)

    # Agar hasil query bisa diakses seperti dictionary
    conn.row_factory = sqlite3.Row

    return conn