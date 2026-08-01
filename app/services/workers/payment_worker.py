import asyncio

from app.database.order_repository import order_repository
from app.services.payment_service import payment_service



class PaymentWorker:


    def __init__(self):

        self.running = False



    async def start(self):

        self.running = True


        print(
            "[PAYMENT WORKER] STARTED"
        )


        while self.running:


            try:


                orders = (
                    order_repository
                    .get_pending_orders()
                )


                for order in orders:


                    print(
                        "[PAYMENT WORKER] CHECK",
                        order["ref_id"]
                    )


                    # =========================
                    # CEK QR ID
                    # =========================

                    qr_id = order.get(
                        "qr_id"
                    )


                    if not qr_id:


                        print(
                            "[QR ID KOSONG]",
                            order["ref_id"]
                        )

                        continue



                    # =========================
                    # CEK PEMBAYARAN QRIS
                    # =========================

                    payment_status = (
                        payment_service
                        .check_payment(
                            qr_id
                        )
                    )



                    if payment_status in [

                        "PAID",
                        "COMPLETED",
                        "SUCCESS"

                    ]:



                        print(
                            "[PAYMENT] PAID",
                            order["ref_id"]
                        )



                        # UPDATE STATUS PEMBAYARAN

                        order_repository.update_payment_status(

                            order["ref_id"],

                            "PAID"

                        )



                        # LOCK ORDER

                        order_repository.update_status(

                            ref_id=order["ref_id"],

                            status="PROCESSING",

                            message="Pembayaran diterima, proses DigiFlazz"

                        )



                        # KIRIM KE DIGIFLAZZ

                        payment_service.process_payment(

                            order

                        )



                    else:



                        print(

                            "[PAYMENT] WAITING",

                            order["ref_id"],

                            payment_status

                        )



            except Exception as e:



                print(

                    "[PAYMENT WORKER ERROR]",

                    e

                )



            await asyncio.sleep(5)



    def stop(self):

        self.running = False





payment_worker = PaymentWorker()