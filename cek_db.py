import sqlite3


conn = sqlite3.connect(
    "storage/bot_database.db"
)


cursor = conn.execute(
    "PRAGMA table_info(orders)"
)


for row in cursor.fetchall():
    print(row)


conn.close()