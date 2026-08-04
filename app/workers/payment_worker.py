import asyncio
import json


from app.database.transaction_repository import (
    transaction_repository
)

from app.services.digiflazz_service import (
    digiflazz
)

from app.bot import bot




# =====================================
# PAYMENT WORKER
# =====================================

class PaymentWorker:


    def __init__(self):

        self.running = True




    # =================================
    # START WORKER
    # =================================

    async def start(self):

        print("[PAYMENT WORKER] STARTED")


        while self.running:


            try:

                await self.process_transactions()


            except Exception as e:

                print(
                    "[PAYMENT WORKER ERROR]",
                    e
                )


            await asyncio.sleep(5)





    # =================================
    # PROCESS TRANSACTIONS
    # =================================

    async def process_transactions(self):


        transactions = (
            transaction_repository
            .get_paid_pending()
        )



        if not transactions:

            return





        for trx in transactions:


            trx_id = trx["trx_id"]


            print(
                "[WORKER PROCESS]",
                trx_id
            )



            try:


                transaction_repository.mark_processing(
                    trx_id
                )



                response = digiflazz.prepaid_transaction(

                    customer_no=trx["customer_no"],

                    buyer_sku_code=trx["product_code"],

                    ref_id=trx_id

                )



                print("======================")
                print("DIGIFLAZZ WORKER RESPONSE")
                print(response)
                print("======================")





                status = (
                    digiflazz
                    .get_status(response)
                )





                # ==========================
                # SUCCESS
                # ==========================

                if status in [
                    "SUKSES",
                    "SUCCESS"
                ]:



                    transaction_repository.mark_success(

                        trx_id,

                        json.dumps(
                            response
                        )

                    )



                    sn = (
                        digiflazz
                        .get_sn(response)
                    )



                    await self.send_success(

                        trx,

                        sn

                    )




                # ==========================
                # FAILED
                # ==========================

                elif status in [
                    "GAGAL",
                    "FAILED"
                ]:


                    transaction_repository.mark_failed(

                        trx_id,

                        json.dumps(
                            response
                        )

                    )



                    await self.send_failed(

                        trx

                    )



            except Exception as e:



                print(
                    "[TRANSACTION ERROR]",
                    trx_id,
                    e
                )





    # =====================================
    # SEND SUCCESS MESSAGE
    # =====================================

    async def send_success(

        self,

        trx,

        sn

    ):


        try:


            await bot.send_message(

                chat_id=trx["telegram_id"],


                text=f"""
✅ PEMBAYARAN BERHASIL


📦 Produk:

{trx['product_name']}


📱 Nomor:

{trx['customer_no']}


🆔 ID:

{trx['trx_id']}


🎫 Token / SN:

{sn or '-'}


Terima kasih telah menggunakan RajaPulsa.
"""

            )


        except Exception as e:


            print(
                "[SEND SUCCESS ERROR]",
                e
            )







    # =====================================
    # SEND FAILED MESSAGE
    # =====================================

    async def send_failed(

        self,

        trx

    ):


        try:


            await bot.send_message(

                chat_id=trx["telegram_id"],


                text=f"""
❌ TRANSAKSI GAGAL


📦 Produk:

{trx['product_name']}


📱 Nomor:

{trx['customer_no']}


🆔 ID:

{trx['trx_id']}


Silakan hubungi admin.
"""

            )


        except Exception as e:


            print(
                "[SEND FAILED ERROR]",
                e
            )





# =====================================
# INSTANCE
# =====================================

payment_worker = PaymentWorker()