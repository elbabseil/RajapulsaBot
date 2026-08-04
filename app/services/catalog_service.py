from collections import defaultdict

from app.database.product_repository import product_repository


class CatalogService:

    def __init__(self):
        self.refresh()


    # =====================================
    # LOAD PRODUCTS
    # =====================================

    def refresh(self):

        self.products = product_repository.get_all()



    # =====================================
    # PRODUCT TYPE FILTER
    # =====================================

    def get_prepaid_products(self):

        prepaid_categories = [

            "Pulsa",
            "Data",
            "Games",
            "Voucher",
            "PLN",
            "Masa Aktif",
            "Aktivasi Perdana",
            "Aktivasi Voucher",
            "Paket SMS & Telpon",
            "eSIM",
            "Gas"

        ]


        return [

            p

            for p in self.products

            if p.get("category") in prepaid_categories

        ]



    def get_postpaid_products(self):

        return [

            p

            for p in self.products

            if p.get("category") == "Pascabayar"

        ]



    # =====================================
    # CATEGORY
    # =====================================

    def get_categories(
        self,
        product_type=None
    ):


        if product_type == "prepaid":

            products = self.get_prepaid_products()


        elif product_type == "postpaid":

            products = self.get_postpaid_products()


        else:

            products = self.products



        return sorted(

            {

                p.get("category")

                for p in products

                if p.get("category")

            }

        )



    # =====================================
    # BRAND
    # =====================================

    def get_brands(
        self,
        category,
        product_type=None
    ):


        if product_type == "prepaid":

            products = self.get_prepaid_products()


        elif product_type == "postpaid":

            products = self.get_postpaid_products()


        else:

            products = self.products



        return sorted(

            {

                p.get("brand")

                for p in products

                if p.get("category") == category

                and p.get("brand")

            }

        )



    # =====================================
    # PRODUCTS
    # =====================================

    def get_products(
        self,
        category,
        brand=None,
        product_type=None
    ):


        if product_type == "prepaid":

            products = self.get_prepaid_products()


        elif product_type == "postpaid":

            products = self.get_postpaid_products()


        else:

            products = self.products



        result = [

            p

            for p in products

            if p.get("category") == category

            and (

                brand is None

                or p.get("brand") == brand

            )

        ]



        return sorted(

            result,

            key=lambda x: x.get(
                "price",
                0
            )

        )



    # =====================================
    # FIND PRODUCT SKU
    # =====================================

    def get_product_by_sku(
        self,
        buyer_sku_code
    ):


        for product in self.products:


            if product.get(
                "buyer_sku_code"
            ) == buyer_sku_code:

                return product



        return None



    # =====================================
    # SEARCH
    # =====================================

    def search(
        self,
        keyword
    ):


        keyword = keyword.lower()



        return [

            p

            for p in self.products

            if keyword in p.get(
                "product_name",
                ""
            ).lower()

        ]



    # =====================================
    # MARKETPLACE
    # =====================================

    def get_marketplace(
        self,
        product_type=None
    ):


        marketplace = defaultdict(dict)



        for category in self.get_categories(
            product_type
        ):


            brands = self.get_brands(

                category,

                product_type

            )



            for brand in brands:


                marketplace[category][brand] = self.get_products(

                    category,

                    brand,

                    product_type

                )



        return dict(
            marketplace
        )



# =====================================
# INSTANCE
# =====================================

catalog_service = CatalogService()