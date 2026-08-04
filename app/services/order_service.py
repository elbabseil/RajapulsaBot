import uuid

from app.database.order_repository import order_repository
from app.database.product_repository import product_repository



class OrderService:


    def __init__(self):

        order_repository.create_table()



    # =========================
    # CREATE ORDER
    # =========================

    def create_order(
        self,
        customer_no,
        buyer_sku_code,
        telegram_id=None
    ):


        # =========================
        # CARI PRODUK
        # =========================

        products = product_repository.get_all()


        product = None


        for p in products:


            sku_database = str(
                p["buyer_sku_code"]
            ).strip().lower()


            sku_request = str(
                buyer_sku_code
            ).strip().lower()


            if sku_database == sku_request:

                product = p

                break



        if not product:


            return {

                "status": "FAILED",

                "message": "Produk tidak ditemukan",

                "buyer_sku_code": buyer_sku_code

            }



        # =========================
        # BUAT REF ID
        # =========================

        ref_id = (

            "RP-"

            + uuid.uuid4().hex[:8].upper()

        )



        # =========================
        # DETAIL PRODUK
        # =========================

        product_name = product["product_name"]

        price = product["price"]



        # =========================
        # STATUS AWAL
        # =========================

        status = "PENDING"


        message = (

            "Order dibuat, "

            "menunggu proses pembayaran"

        )



        # =========================
        # SIMPAN DATABASE
        # =========================

        order_repository.save_order(

            ref_id=ref_id,

            customer_no=customer_no,

            buyer_sku_code=buyer_sku_code,

            product_name=product_name,

            price=price,

            status=status,

            message=message,

            sn=None,

            telegram_id=telegram_id

        )



        # =========================
        # RESPONSE
        # =========================

        return {


            "ref_id": ref_id,


            "status": status,


            "product_name": product_name,


            "price": price,


            "customer_no": customer_no,


            "buyer_sku_code": buyer_sku_code,


            "telegram_id": telegram_id,


            "message": message

        }


    # =========================
    # CREATE ORDER WEBSITE
    # =========================

    def create_order_by_product_id(
        self,
        customer_no,
        product_id
    ):


        products = product_repository.get_all()


        product = None


        for p in products:

            if p["id"] == product_id:

                product = p
                break



        if not product:

            return {

                "status": "FAILED",

                "message": "Produk tidak ditemukan"

            }



        ref_id = (

            "RP-"

            + uuid.uuid4().hex[:8].upper()

        )



        product_name = (

            product.get("product_name")

            or product.get("name")

        )


        price = product.get("price")


        buyer_sku_code = product.get(
            "buyer_sku_code"
        )



        order_repository.save_order(

            ref_id=ref_id,

            customer_no=customer_no,

            buyer_sku_code=buyer_sku_code,

            product_name=product_name,

            price=price,

            status="PENDING",

            message="Order website menunggu pembayaran",

            sn=None,

            telegram_id=None

        )


        return {

            "status":"SUCCESS",

            "ref_id":ref_id,

            "product_name":product_name,

            "price":price,

            "customer_no":customer_no

        }


order_service = OrderService()