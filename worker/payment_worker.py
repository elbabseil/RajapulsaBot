import threading
import time
import logging


from app.database.transaction_repository import transaction_repository
from app.services.digiflazz_service import digiflazz



class PaymentWorker:


    def __init__(self):

        self.running = False



    # ============================
    # START
    # ============================

    def start(self):

        if self.running:
            return


        self.running = True


        thread = threading.Thread(

            target=self.run,

            daemon=True

        )


        thread.start()


        print(
            "[PAYMENT WORKER] STARTED"
        )



    # ============================
    # LOOP
    # ============================

    def run(self):


        while self.running:


            try:

                self.process_payment()


            except Exception as e:

                logging.error(
                    e
                )


            time.sleep(5)




    # ============================
    # PROCESS PAYMENT
    # ============================

    def process_payment(self):


        transactions = (

            transaction_repository
            .get_paid_pending()

        )


        for trx in transactions:


            trx_id = trx["trx_id"]


            print(
                "[WORKER PROCESS]",
                trx_id
            )



            transaction_repository.update_status(

                trx_id=trx_id,

                transaction_status="PROCESSING"

            )



            self.send_digiflazz(trx)






    # ============================
    # SEND DIGIFLAZZ
    # ============================

    def send_digiflazz(
        self,
        trx
    ):


        try:


            product_type = str(

                trx.get(

                    "product_type",

                    ""

                )

            ).upper()



            print(
                "[PRODUCT TYPE]",
                product_type
            )



            # ======================
            # PASCABAYAR
            # ======================

            if product_type == "PASCABAYAR":


                response = digiflazz.pasca_transaction(

                    customer_no=

                    trx["customer_no"],


                    buyer_sku_code=

                    trx["product_code"],


                    ref_id=

                    trx["trx_id"]

                )



            # ======================
            # PREPAID
            # ======================

            else:


                response = digiflazz.prepaid_transaction(

                    customer_no=

                    trx["customer_no"],


                    buyer_sku_code=

                    trx["product_code"],


                    ref_id=

                    trx["trx_id"]

                )




            print(
                "[DIGIFLAZZ RESPONSE]",
                response
            )



            if not response:


                self.failed(

                    trx,

                    "EMPTY RESPONSE"

                )

                return





            data = response.get(

                "data",

                {}

            )



            status = str(

                data.get(

                    "status",

                    ""

                )

            ).upper()





            # ======================
            # SUCCESS
            # ======================

            if status in [

                "SUCCESS",

                "SUKSES"

            ]:


                transaction_repository.update_status(

                    trx_id=

                    trx["trx_id"],


                    transaction_status=

                    "SUCCESS",


                    response=str(response)

                )


                print(

                    "[SUCCESS]",

                    trx["trx_id"]

                )






            # ======================
            # PENDING
            # ======================

            elif status == "PENDING":


                transaction_repository.update_status(

                    trx_id=

                    trx["trx_id"],


                    transaction_status=

                    "PENDING",


                    response=str(response)

                )





            # ======================
            # FAILED
            # ======================

            else:


                self.failed(

                    trx,

                    str(response)

                )





        except Exception as e:


            self.failed(

                trx,

                str(e)

            )






    # ============================
    # FAILED
    # ============================

    def failed(

        self,

        trx,

        message

    ):


        transaction_repository.update_status(

            trx_id=

            trx["trx_id"],


            transaction_status=

            "FAILED",


            response=

            message

        )


        print(

            "[FAILED]",

            trx["trx_id"],

            message

        )





payment_worker = PaymentWorker()