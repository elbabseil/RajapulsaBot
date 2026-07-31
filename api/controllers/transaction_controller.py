from app.services.transaction_service import transaction_service
from app.database.product_repository import product_repository


def buy_product(
    telegram_id,
    buyer_sku_code,
    customer_no
):

    products = product_repository.get_all()

    print("TOTAL PRODUK:", len(products))
    print("SKU DICARI :", buyer_sku_code)

    for item in products:
        if item["buyer_sku_code"] == buyer_sku_code:
            print("PRODUK DITEMUKAN:", item)
            return transaction_service.buy_product(
                telegram_id,
                item,
                customer_no
            )

    print("PRODUK TIDAK DITEMUKAN")

    return {
        "success": False,
        "message": "Produk tidak ditemukan"
    }