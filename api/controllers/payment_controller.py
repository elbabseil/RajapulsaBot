from fastapi import APIRouter, Request, HTTPException

from app.services.xendit_service import xendit
from app.database.transaction_repository import transaction_repository


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)



# ===================================
# CREATE QRIS PAYMENT
# ===================================

@router.post("/create-qris")
def create_qris(
    transaction_id: str,
    amount: int
):


    print("==============================")
    print("[CREATE QRIS]")
    print("TRX ID :", transaction_id)
    print("AMOUNT :", amount)
    print("==============================")


    if amount <= 0:

        raise HTTPException(
            status_code=400,
            detail="Amount tidak valid"
        )



    # =================================
    # CEK TRANSAKSI
    # =================================

    trx = transaction_repository.get_by_trx_id(
        transaction_id
    )



    # =================================
    # BUAT TRANSAKSI JIKA BELUM ADA
    # =================================

    if not trx:


        transaction_repository.create(

            trx_id=transaction_id,

            telegram_id="SYSTEM",

            product_code="QRIS",

            product_name="Pembayaran QRIS",

            customer_no="-",

            price=amount,

            payment_method="QRIS"

        )


        print(
            "[DATABASE] TRANSAKSI BARU DIBUAT"
        )



    else:

        print(
            "[DATABASE] TRANSAKSI SUDAH ADA"
        )





    # =================================
    # CREATE QRIS XENDIT
    # =================================

    result = xendit.create_qris(

        transaction_id,

        amount

    )



    if not result:


        return {


            "success":False,


            "message":
            "Gagal membuat QRIS"


        }





    print("==============================")
    print("[XENDIT QRIS RESPONSE]")
    print(result)
    print("==============================")





    # =================================
    # SIMPAN DATA QRIS
    # =================================


    transaction_repository.save_qris(


        trx_id=transaction_id,


        qris_id=result.get(
            "id"
        ),


        qr_string=result.get(
            "qr_string"
        ),


        expired=(

            result.get(
                "expires_at"
            )

            or

            result.get(
                "expiry_date"
            )

        )

    )



    print(
        "[DATABASE] QRIS DATA SAVED"
    )





    return {


        "success":True,


        "trx_id":transaction_id,


        "payment":result


    }







# ===================================
# XENDIT CALLBACK WEBHOOK
# ===================================


@router.post("/callback")
async def xendit_callback(

    request:Request

):


    data = await request.json()



    print("==============================")
    print("[XENDIT CALLBACK]")
    print(data)
    print("==============================")




    external_id = (

        data.get(
            "external_id"
        )

        or

        data.get(
            "reference_id"
        )

    )



    status = str(

        data.get(
            "status",
            ""
        )

    ).upper()





    if not external_id:


        return {


            "success":False,


            "message":
            "external id kosong"


        }






    trx = transaction_repository.get_by_trx_id(

        external_id

    )




    if not trx:


        print(
            "[WARNING] TRANSAKSI TIDAK ADA",
            external_id
        )


        return {


            "success":False,


            "message":
            "trx tidak ditemukan"


        }







    # =================================
    # PAYMENT SUCCESS
    # =================================


    if status in [

        "PAID",

        "COMPLETED",

        "SUCCESS",

        "SUCCEEDED"

    ]:



        transaction_repository.update_status(

            trx_id=external_id,

            payment_status="PAID",

            transaction_status="PENDING"

        )



        print("==============================")
        print("[PAYMENT BERHASIL]")
        print(external_id)
        print("==============================")



        # =================================
        # NANTI PAYMENT WORKER DISINI
        #
        # worker.process_paid_transaction(
        #       external_id
        # )
        #
        # =================================




    else:



        transaction_repository.update_status(

            trx_id=external_id,

            payment_status=status

        )



        print(
            "[PAYMENT STATUS]",
            status
        )






    return {


        "success":True,


        "trx_id":external_id,


        "status":status


    }