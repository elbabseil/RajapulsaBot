
from app.services.xendit_service import xendit

from app.services.digiflazz_service import (
    digiflazz
)


from app.database.transaction_repository import (
    transaction_repository
)


from app.database.order_repository import (
    order_repository
)




class PaymentService:



    # =====================================
    # CREATE QRIS
    # =====================================

    def create_qris_payment(
        self,
        order
    ):


        ref_id = order["ref_id"]

        price = order["price"]



        qris = xendit.create_qris(

            ref_id,

            price

        )



        if not qris:

            return None



        qr_string = (

            qris.get("qr_string")

            or

            qris.get("qr_code")

            or

            qris.get("qr")

        )



        if not qr_string:

            return None



        qris_id = qris.get(
            "id"
        )



        transaction_repository.save_qris(

            ref_id,

            qris_id,

            qr_string

        )



        order_repository.update_qr_id(

            ref_id,

            qris_id

        )



        return {

            "qris_id":
            qris_id,


            "qr_string":
            qr_string

        }






    # =====================================
    # CEK STATUS QRIS
    # =====================================

    def check_payment(

        self,

        qris_id

    ):


        result = xendit.get_qris_status(

            qris_id

        )



        if not result:

            return None



        return str(

            result.get(
                "status",
                ""
            )

        ).upper()






    # =====================================
    # PROSES SETELAH BAYAR
    # =====================================

    def process_payment(

        self,

        order

    ):


        ref_id = order["ref_id"]


        customer_no = order.get(
            "customer_no"
        )


        sku = order.get(
            "buyer_sku_code"
        )



        # ambil kategori dari SKU
        product_name = order.get(
            "product_name",
            ""
        )



        print(
            "[DIGIFLAZZ PROCESS]",
            ref_id,
            sku,
            customer_no
        )



        try:


            # =============================
            # PASCA BAYAR
            # =============================

            if "Tagihan" in product_name:

                result = digiflazz.pasca_transaction(

                    customer_no,

                    sku,

                    ref_id

                )


            else:


                # =============================
                # PREPAID
                # Pulsa
                # Data
                # Game
                # Token PLN
                # Voucher
                # =============================

                result = digiflazz.prepaid_transaction(

                    customer_no,

                    sku,

                    ref_id

                )



            print(
                "[DIGIFLAZZ RESULT]",
                result
            )



            if not result:


                order_repository.update_status(

                    ref_id,

                    "FAILED",

                    "Provider tidak merespon"

                )


                return False





            status = digiflazz.get_status(

                result

            )



            message = digiflazz.get_message(

                result

            )



            sn = digiflazz.get_sn(

                result

            )




            if status in [

                "SUCCESS",

                "SUKSES"

            ]:



                order_repository.update_status(

                    ref_id,

                    "SUCCESS",

                    message,

                    sn,

                    str(result)

                )



            elif status in [

                "PENDING"

            ]:



                order_repository.update_status(

                    ref_id,

                    "PROCESSING",

                    message,

                    sn,

                    str(result)

                )



            else:



                order_repository.update_status(

                    ref_id,

                    "FAILED",

                    message,

                    sn,

                    str(result)

                )



            return True



        except Exception as e:



            print(
                "[PROCESS PAYMENT ERROR]",
                e
            )



            order_repository.update_status(

                ref_id,

                "FAILED",

                str(e)

            )


            return False





payment_service = PaymentService()