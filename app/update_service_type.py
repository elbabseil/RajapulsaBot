import sqlite3


conn = sqlite3.connect(
    "storage/bot_database.db"
)


cursor = conn.cursor()


# ==========================
# PREPAID
# ==========================

cursor.execute("""
UPDATE products

SET service_type = 'PREPAID'

WHERE category IN (

    'Aktivasi Perdana',
    'Aktivasi Voucher',
    'Data',
    'Games',
    'Masa Aktif',
    'PLN',
    'Paket SMS & Telpon',
    'Pulsa',
    'Voucher',
    'eSIM'

)
""")


# ==========================
# POSTPAID
# ==========================

cursor.execute("""
UPDATE products

SET service_type = 'POSTPAID'

WHERE category IN (

    'Pascabayar',
    'Gas',
    'TV'

)
""")


conn.commit()


print("SERVICE TYPE UPDATED")


conn.close()