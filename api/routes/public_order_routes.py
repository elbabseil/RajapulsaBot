from fastapi import APIRouter

from app.database.product_repository import product_repository
from app.database.transaction_repository import transaction_repository
from app.services.order_service import order_service
from app.services.xendit_service import xendit


router = APIRouter(
    prefix="/public",
    tags=["Public Order"]
)


# =====================================
# CREATE PUBLIC ORDER
# =====================================

@router.post("/order")
def create_public_order(data: dict):

    try:

        product_id = data.get("product_id")
        customer_no = data.get("customer_no")


        if not product_id or not customer_no:

            return {

                "status": "FAILED",

                "message":
                "product_id dan customer_no wajib diisi"

            }



        # ==========================
        # CARI PRODUK
        # ==========================

        products = product_repository.get_all()


        product = None


        for p in products:

            if p["id"] == product_id:

                product = p

                break



        if not product:

            return {

                "status": "FAILED",

                "message":
                "Produk tidak ditemukan"

            }



        # ==========================
        # CREATE ORDER
        # ==========================

        order = order_service.create_order(

            customer_no=customer_no,

            buyer_sku_code=
            product["buyer_sku_code"],

            telegram_id=None

        )



        if order.get("status") == "FAILED":

            return order



        trx_id = order["ref_id"]



        # ==========================
        # CREATE TRANSACTION
        # ==========================

        transaction_repository.create(

            trx_id=trx_id,

            telegram_id="PUBLIC",

            product_code=
            product["buyer_sku_code"],

            product_name=
            product["product_name"],

            customer_no=
            customer_no,

            price=
            product["price"],

            payment_method="QRIS"

        )



        # ==========================
        # RESPONSE
        # ==========================

        return {


            "status":
            "SUCCESS",


            "order":
            order,


            "payment":{


                "method":
                "QRIS",


                "trx_id":
                trx_id,


                "qr_string":
                None,


                "expires_at":
                None


            }


        }



    except Exception as e:


        return {


            "status":
            "ERROR",


            "message":
            str(e)


        }





# =====================================
# CHECK ORDER STATUS
# =====================================

@router.get("/order/status/{trx_id}")
def order_status(trx_id: str):

    try:


        trx = transaction_repository.get_by_trx_id(

            trx_id

        )



        if not trx:


            return {


                "status":
                "FAILED",


                "message":
                "Transaksi tidak ditemukan"


            }





        return {


            "status":
            "SUCCESS",


            "transaction":{


                "trx_id":
                trx["trx_id"],


                "product_name":
                trx["product_name"],


                "customer_no":
                trx["customer_no"],


                "price":
                trx["price"],


                "payment_method":
                trx["payment_method"],


                "payment_status":
                trx["payment_status"],


                "transaction_status":
                trx["transaction_status"],


                "qris_id":
                trx["qris_id"],


                "qr_string":
                trx["qr_string"],


                "expired":
                trx["payment_expired"]


            }


        }



    except Exception as e:


        return {


            "status":
            "ERROR",


            "message":
            str(e)


        }