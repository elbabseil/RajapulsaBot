import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from ppob_service import get_digiflazz_price_list
from app.repositories.product_repository import save_product


def normalize_category(name):

    name = name.lower()

    if "pulsa" in name:
        return "Pulsa"

    if "internet" in name or "data" in name:
        return "Paket Internet"

    if "pln" in name:
        return "Token PLN"

    if "game" in name or "voucher" in name:
        return "Voucher Game"

    return "Lainnya"



def sync_products():

    print("Mengambil produk Digiflazz...")

    products = get_digiflazz_price_list()

    if not products:
        print("Produk kosong")
        return


    total = 0

    for item in products:

        product = {

            "sku":
                item.get("buyer_sku_code"),


            "name":
                item.get("product_name"),


            "category":
                normalize_category(
                    item.get("product_name", "")
                ),


            "brand":
                item.get("brand",""),


            "price":
                item.get("price",0),


            "selling_price":
                item.get("price",0) + 1000
        }


        save_product(product)

        total += 1


    print(
        f"Sinkron selesai. {total} produk masuk database."
    )



if __name__ == "__main__":
    sync_products()