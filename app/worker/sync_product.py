from ppob_service import prepaid_price_list
from app.repositories.product_repository import save_product


def normalize_category(product):

    name = product["product_name"].lower()


    if "pulsa" in name:
        return "Pulsa"


    if "internet" in name or "data" in name:
        return "Paket Internet"


    if "pln" in name:
        return "Token PLN"


    if "game" in name:
        return "Voucher Game"


    return "Lainnya"



def sync_products():

    products = prepaid_price_list()


    for item in products:

        product = {

            "sku": item["buyer_sku_code"],

            "name":
            item["product_name"],

            "category":
            normalize_category(item),

            "brand":
            item.get("brand",""),

            "price":
            item["price"],


            "selling_price":
            item["price"] + 1000
        }


        save_product(product)



if __name__ == "__main__":
    sync_products()