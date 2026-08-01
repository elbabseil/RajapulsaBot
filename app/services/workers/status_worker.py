import asyncio

from app.database.order_repository import order_repository
from app.services.digiflazz_service import digiflazz



class StatusWorker:


    def __init__(self):

        self.running = False



    async def start(self):

        self.running = True


        print(
            "[STATUS WORKER] STARTED"
        )



        while self.running:


            try:


                orders = (
                    order_repository
                    .get_processing_orders()
                )



                for order in orders:


                    ref_id = order["ref_id"]



                    print(
                        "[STATUS WORKER] CHECK",
                        ref_id
                    )



                    response = (
                        digiflazz
                        .check_transaction_status(

                            customer_no=
                            order["customer_no"],


                            buyer_sku_code=
                            order["buyer_sku_code"],


                            ref_id=
                            ref_id

                        )
                    )



                    if not response:


                        print(
                            "[DIGIFLAZZ STATUS] NO RESPONSE",
                            ref_id
                        )


                        continue




                    status = (
                        digiflazz
                        .get_status(
                            response
                        )
                    )



                    sn = (
                        digiflazz
                        .get_sn(
                            response
                        )
                    )



                    print(
                        "[DIGIFLAZZ STATUS]",
                        status
                    )





                    # =========================
                    # SUCCESS
                    # =========================

                    if status in [

                        "SUCCESS",

                        "SUKSES"

                    ]:


                        order_repository.update_status(

                            ref_id=

                            ref_id,


                            status=

                            "SUCCESS",


                            message=

                            "Transaksi berhasil",


                            sn=

                            sn,


                            provider_response=

                            str(response)

                        )



                        print(
                            "[ORDER SUCCESS]",
                            ref_id
                        )







                    # =========================
                    # FAILED
                    # =========================

                    elif status in [

                        "FAILED",

                        "GAGAL"

                    ]:



                        order_repository.update_status(

                            ref_id=

                            ref_id,


                            status=

                            "FAILED",


                            message=

                            "Transaksi gagal",


                            provider_response=

                            str(response)

                        )



                        print(
                            "[ORDER FAILED]",
                            ref_id
                        )







                    # =========================
                    # PENDING
                    # =========================

                    else:


                        retry = (

                            order_repository

                            .get_retry_count(

                                ref_id

                            )

                        )



                        print(

                            "[STATUS PENDING]",

                            ref_id,

                            "RETRY",

                            retry

                        )





                        if retry >= 10:



                            order_repository.update_status(

                                ref_id=

                                ref_id,


                                status=

                                "FAILED",


                                message=

                                "Timeout DigiFlazz",


                                provider_response=

                                str(response)

                            )



                            print(

                                "[ORDER TIMEOUT]",

                                ref_id

                            )





                        else:



                            order_repository.increase_retry(

                                ref_id

                            )



                            order_repository.update_status(

                                ref_id=

                                ref_id,


                                status=

                                "PROCESSING",


                                message=

                                "Masih diproses DigiFlazz",


                                provider_response=

                                str(response)

                            )





            except Exception as e:


                print(
                    "[STATUS WORKER ERROR]",
                    e
                )



            await asyncio.sleep(10)





    def stop(self):

        self.running = False





status_worker = StatusWorker()