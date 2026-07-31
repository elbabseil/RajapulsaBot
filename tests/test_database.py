from app.database import (
    init_db,
    save_transaction,
    get_transaction,
    update_status,
    get_user_transactions,
)

def main():
    print("=== TEST DATABASE ===")

    # Membuat database dan tabel
    init_db()
    print("✓ Database berhasil dibuat")

    # Simpan transaksi contoh
    save_transaction(
        trx_id="TEST001",
        user_id=123456789,
        product_name="Pulsa Telkomsel 10K",
        phone_number="081234567890",
        nominal=10000,
        status="PENDING"
    )
    print("✓ Simpan transaksi berhasil")

    # Ambil transaksi
    trx = get_transaction("TEST001")
    print("✓ Data transaksi:")
    print(trx)

    # Update status
    update_status("TEST001", "SUCCESS")
    print("✓ Status berhasil diubah")

    # Ambil riwayat
    history = get_user_transactions(123456789)
    print("✓ Riwayat transaksi:")
    print(history)

    print("\n=== TEST SELESAI ===")


if __name__ == "__main__":
    main()