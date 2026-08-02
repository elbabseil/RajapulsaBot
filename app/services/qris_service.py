from app.services.xendit_service import xendit

from app.database.transaction_repository import (
    transaction_repository
)

from app.database.order_repository import (
    order_repository
)



class QRISService:


    def create_qris(
        self,
        trx_id,
        price
    ):


        qris = xendit.create_qris(
            trx_id,
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

            trx_id,

            qris_id,

            qr_string

        )


        order_repository.update_qr_id(

            trx_id,

            qris_id

        )


        return {

            "qris_id":qris_id,

            "qr_string":qr_string

        }



qris_service = QRISService()