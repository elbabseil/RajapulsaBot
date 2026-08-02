from app.services.digiflazz_service import digiflazz
from app.database.order_repository import order_repository
import uuid



class TransactionService:


    # =====================================
    # BUY PRODUCT
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
            # SIMPAN ORDER AWAL
            # =========================

            order_repository.save_order(

                ref_id,

                customer_no,

                product["buyer_sku_code"],

                product["product_name"],

                product["price"],

                "PENDING",

                "Menunggu proses DigiFlazz",

                None,

                telegram_id

            )


            print("==============================")
            print("SAVE ORDER BERHASIL")
            print("==============================")


            order = {

                "ref_id": ref_id,

                "customer_no": customer_no,

                "buyer_sku_code":
                product["buyer_sku_code"]

            }



            # =========================
            # KIRIM DIGIFLAZZ
            # =========================

            result = self.process_order(order)



            return {


                "success": True,


                "ref_id": ref_id,


                "product":
                product["product_name"],


                "status":
                result["status"],


                "message":
                result["message"]


            }




        except Exception as e:


            print("==============================")
            print("BUY PRODUCT ERROR")
            print(e)
            print("==============================")


            return {


                "success": False,


                "message": str(e)


            }







    # =====================================
    # PROCESS DIGIFLAZZ
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



            print("==============================")
            print("RESPONSE DIGIFLAZZ")
            print(response)
            print("==============================")


            if not response:


                order_repository.update_status(

                    ref_id,

                    "FAILED",

                    "Response DigiFlazz kosong",

                    None,

                    "EMPTY RESPONSE"

                )


                return {


                    "status": "FAILED",


                    "message":
                    "Response DigiFlazz kosong"


                }






            status = digiflazz.get_status(response)


            message = digiflazz.get_message(response)


            sn = digiflazz.get_sn(response)




            print("==============================")
            print("STATUS :", status)
            print("MESSAGE :", message)
            print("SN :", sn)
            print("==============================")







            # =========================
            # SUCCESS
            # =========================

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


                    "status": "SUCCESS",


                    "message":
                    "Transaksi berhasil"


                }








            # =========================
            # FAILED
            # =========================

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


                    "status": "FAILED",


                    "message":
                    message


                }









            # =========================
            # PENDING / PROCESSING
            # =========================

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
                    "Transaksi sedang diproses DigiFlazz"


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