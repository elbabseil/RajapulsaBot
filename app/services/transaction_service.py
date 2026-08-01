from app.services.digiflazz_service import digiflazz
from app.database.order_repository import order_repository



class TransactionService:


    def process_order(self, order):


        ref_id = order["ref_id"]


        try:


            response = digiflazz.prepaid_transaction(

                customer_no=order["customer_no"],

                buyer_sku_code=order["buyer_sku_code"],

                ref_id=ref_id

            )


            if not response:


                order_repository.update_status(

                    ref_id=ref_id,

                    status="FAILED",

                    message="Tidak ada response dari DigiFlazz",

                    provider_response=None

                )


                return False




            status = digiflazz.get_status(
                response
            )


            sn = digiflazz.get_sn(
                response
            )



            # =========================
            # SUCCESS
            # =========================

            if status in [
                "SUKSES",
                "SUCCESS"
            ]:


                order_repository.update_status(

                    ref_id=ref_id,

                    status="SUCCESS",

                    message="Transaksi berhasil",

                    sn=sn,

                    provider_response=str(response)

                )



            # =========================
            # FAILED
            # =========================

            elif status in [
                "GAGAL",
                "FAILED"
            ]:


                order_repository.update_status(

                    ref_id=ref_id,

                    status="FAILED",

                    message="Transaksi gagal",

                    provider_response=str(response)

                )



            # =========================
            # PENDING PROVIDER
            # =========================

            else:


                order_repository.update_status(

                    ref_id=ref_id,

                    status="PROCESSING",

                    message="Menunggu status DigiFlazz",

                    provider_response=str(response)

                )



            return True



        except Exception as e:



            order_repository.update_status(

                ref_id=ref_id,

                status="FAILED",

                message=str(e),

                provider_response=str(e)

            )


            return False





transaction_service = TransactionService()