from app.services.transaction_service import transaction_service
from app.services.xendit_service import xendit



class PaymentService:


    def create_payment(self, order):

        return {

            "status": "PENDING",

            "ref_id": order["ref_id"],

            "message": "Menunggu proses pembayaran"

        }



    def check_payment(self, qr_id):

        try:


            result = (
                xendit
                .get_qris_status(
                    qr_id
                )
            )


            if not result:

                return "UNPAID"



            status = result.get(
                "status"
            )


            print(
                "[PAYMENT STATUS]",
                status
            )


            return status or "UNPAID"



        except Exception as e:


            print(
                "[CHECK PAYMENT ERROR]",
                e
            )


            return "UNPAID"



    def process_payment(self, order):

        return transaction_service.process_order(
            order
        )



payment_service = PaymentService()