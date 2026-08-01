from collections import defaultdict

from app.database.product_repository import product_repository


class CatalogService:

    def __init__(self):
        self.refresh()


    def refresh(self):

        self.products = product_repository.get_all()



    def get_categories(self):

        return sorted(
            {
                p["category"]
                for p in self.products
                if p.get("category")
            }
        )



    def get_brands(self, category):

        return sorted(
            {
                p["brand"]
                for p in self.products
                if p.get("category") == category
                and p.get("brand")
            }
        )



    def get_products(self, category, brand=None):

        return sorted(

            [

                p

                for p in self.products

                if p.get("category") == category

                and (
                    brand is None
                    or p.get("brand") == brand
                )

            ],

            key=lambda x: x.get("price", 0)

        )



    def get_product_by_sku(self, buyer_sku_code):

        for product in self.products:

            if product["buyer_sku_code"] == buyer_sku_code:

                return product

        return None



    def search(self, keyword):

        keyword = keyword.lower()


        return [

            p

            for p in self.products

            if keyword in p["product_name"].lower()

        ]



    def get_marketplace(self):

        marketplace = defaultdict(dict)


        for category in self.get_categories():

            for brand in self.get_brands(category):

                marketplace[category][brand] = self.get_products(
                    category,
                    brand
                )


        return dict(marketplace)



catalog_service = CatalogService()