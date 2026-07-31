from app.database.product_repository import product_repository
from app.services.digiflazz_service import digiflazz


class ProductService:


    def __init__(self):
        product_repository.create_table()



    def sync(self):

        print("[SYNC] Mengambil produk DigiFlazz...")


        prepaid = digiflazz.prepaid_price_list()

        if not isinstance(prepaid, list):
            prepaid = []


        pasca = digiflazz.pasca_price_list()

        if not isinstance(pasca, list):
            pasca = []


        products = prepaid + pasca


        if products:
            product_repository.save_products(products)


        print(
            f"[SYNC] Tersimpan {len(products)} produk"
        )


        return {
            "prepaid": len(prepaid),
            "pasca": len(pasca),
            "total": len(products)
        }



    def get_all_products(self):

        return product_repository.get_all()



    def get_prepaid_products(self):

        return product_repository.get_prepaid()



    def get_pasca_products(self):

        return product_repository.get_pasca()



product_service = ProductService()



def get_products():

    return product_service.get_all_products()