from app.services.digiflazz_service import digiflazz
from app.database.order_repository import order_repository
import uuid


class TransactionService:


    # =====================================
    # CREATE BUY ORDER
    # =====================================

    def buy_product(
        self,
        telegram_id,
        product,
        customer_no
    ):

        print("==============================")
        print("SERVICE BUY PRODUCT MASUK")
        print(product)
        print(customer_no)
        print("==============================")


        ref_id = (
            "RP-"
            +
            str(uuid.uuid4())[:8].upper()
        )


        print("REF ID:", ref_id)


        try:


            # =========================
            # SIMPAN ORDER
            # =========================

            order_repository.save_order(

                ref_id,

                customer_no,

                product["buyer_sku_code"],

                product["product_name"],

                product["price"],

                "PENDING",

                "Menunggu pembayaran",

                None,

                telegram_id

            )


            print("==============================")
            print("ORDER DISIMPAN")
            print("==============================")


            return {


                "success": True,


                "ref_id": ref_id,


                "product":
                product["product_name"],


                "amount":
                product["price"],


                "status":
                "PENDING",


                "payment_status":
                "UNPAID",


                "message":
                "Menunggu pembayaran"



            }



        except Exception as e:


            print("==============================")
            print("CREATE ORDER ERROR")
            print(e)
            print("==============================")


            return {


                "success": False,


                "message": str(e)


            }





    # =====================================
    # PROCESS DIGIFLAZZ AFTER PAYMENT
    # =====================================

    def process_order(
        self,
        order
    ):


        ref_id = order["ref_id"]


        try:


            print("==============================")
            print("KIRIM DIGIFLAZZ")
            print(order)
            print("==============================")


            response = digiflazz.prepaid_transaction(

                customer_no=
                order["customer_no"],


                buyer_sku_code=
                order["buyer_sku_code"],


                ref_id=
                ref_id

            )


            print("RESPONSE DIGIFLAZZ")
            print(response)



            if not response:


                order_repository.update_status(

                    ref_id,

                    "FAILED",

                    "Response DigiFlazz kosong",

                    None,

                    "EMPTY RESPONSE"

                )


                return {


                    "status":
                    "FAILED",


                    "message":
                    "Response DigiFlazz kosong"


                }



            status = digiflazz.get_status(response)

            message = digiflazz.get_message(response)

            sn = digiflazz.get_sn(response)



            print("STATUS :", status)
            print("MESSAGE :", message)
            print("SN :", sn)



            if status in [

                "SUKSES",
                "SUCCESS"

            ]:


                order_repository.update_status(

                    ref_id,

                    "SUCCESS",

                    message,

                    sn,

                    str(response)

                )


                return {


                    "status":
                    "SUCCESS",


                    "message":
                    "Transaksi berhasil"


                }





            elif status in [

                "GAGAL",
                "FAILED"

            ]:


                order_repository.update_status(

                    ref_id,

                    "FAILED",

                    message,

                    None,

                    str(response)

                )


                return {


                    "status":
                    "FAILED",


                    "message":
                    message


                }




            else:


                order_repository.update_status(

                    ref_id,

                    "PROCESSING",

                    message,

                    None,

                    str(response)

                )


                return {


                    "status":
                    "PROCESSING",


                    "message":
                    "Transaksi sedang diproses"



                }



        except Exception as e:


            print("==============================")
            print("DIGIFLAZZ ERROR")
            print(e)
            print("==============================")


            order_repository.update_status(

                ref_id,

                "FAILED",

                str(e),

                None,

                str(e)

            )


            return {


                "status":
                "FAILED",


                "message":
                str(e)


            }




transaction_service = TransactionService()