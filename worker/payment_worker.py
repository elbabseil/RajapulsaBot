import threading
import time
import logging

from app.database.transaction_repository import transaction_repository
from app.services.digiflazz_service import digiflazz
from app.services.catalog_service import catalog_service


class PaymentWorker:

    def __init__(self):
        self.running = False

    # =====================================
    # START
    # =====================================

    def start(self):

        if self.running:
            return

        self.running = True

        thread = threading.Thread(
            target=self.run,
            daemon=True
        )

        thread.start()

        print("[PAYMENT WORKER] STARTED")

    # =====================================
    # LOOP
    # =====================================

    def run(self):

        while self.running:

            try:
                self.process_payment()

            except Exception as e:
                logging.exception(e)

            time.sleep(5)

    # =====================================
    # PROCESS PAYMENT
    # =====================================

    def process_payment(self):

        transactions = transaction_repository.get_paid_pending()

        if not transactions:
            return

        for trx in transactions:

            trx_id = trx["trx_id"]

            print("==============================")
            print("[WORKER PROCESS]")
            print(trx_id)
            print("==============================")

            transaction_repository.mark_processing(
                trx_id
            )

            self.send_digiflazz(trx)

    # =====================================
    # SEND DIGIFLAZZ
    # =====================================

    def send_digiflazz(self, trx):

        try:

            # ===============================
            # AMBIL PRODUK DARI KATALOG
            # ===============================

            product = catalog_service.get_product_by_sku(
                trx["product_code"]
            )

            if not product:

                self.failed(
                    trx,
                    "PRODUCT NOT FOUND"
                )

                return

            service_type = str(
                product.get(
                    "service_type",
                    "PREPAID"
                )
            ).upper()

            print("==============================")
            print("[PRODUCT]")
            print(product["product_name"])
            print("[SERVICE TYPE]")
            print(service_type)
            print("==============================")

            # ===============================
            # POSTPAID
            # ===============================

            if service_type == "POSTPAID":

                response = digiflazz.pasca_transaction(

                    customer_no=trx["customer_no"],

                    buyer_sku_code=trx["product_code"],

                    ref_id=trx["trx_id"]

                )

            # ===============================
            # PREPAID
            # ===============================

            else:

                response = digiflazz.prepaid_transaction(

                    customer_no=trx["customer_no"],

                    buyer_sku_code=trx["product_code"],

                    ref_id=trx["trx_id"]

                )

            print("==============================")
            print("[DIGIFLAZZ RESPONSE]")
            print(response)
            print("==============================")

            if not response:

                self.failed(
                    trx,
                    "EMPTY RESPONSE"
                )

                return

            data = response.get("data", {})

            status = str(
                data.get(
                    "status",
                    ""
                )
            ).upper()

            # ===============================
            # SUCCESS
            # ===============================

            if status in ("SUCCESS", "SUKSES"):

                transaction_repository.mark_success(
                    trx["trx_id"],
                    str(response)
                )

                print(
                    "[SUCCESS]",
                    trx["trx_id"]
                )

            # ===============================
            # PENDING
            # ===============================

            elif status == "PENDING":

                transaction_repository.update_status(

                    trx_id=trx["trx_id"],

                    transaction_status="PENDING",

                    response=str(response)

                )

                print(
                    "[PENDING]",
                    trx["trx_id"]
                )

            # ===============================
            # FAILED
            # ===============================

            else:

                self.failed(
                    trx,
                    str(response)
                )

        except Exception as e:

            logging.exception(e)

            self.failed(
                trx,
                str(e)
            )

    # =====================================
    # FAILED
    # =====================================

    def failed(
        self,
        trx,
        message
    ):

        transaction_repository.mark_failed(
            trx["trx_id"],
            message
        )

        print(
            "[FAILED]",
            trx["trx_id"],
            message
        )


payment_worker = PaymentWorker()