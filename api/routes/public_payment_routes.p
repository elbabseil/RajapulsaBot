from fastapi import APIRouter, HTTPException

from app.database.order_repository import order_repository
from app.services.xendit_service import xendit


router = APIRouter(
    prefix="/public",
    tags=["Public Payment"]
)



@router.post("/payment/{ref_id}")
def create_payment(ref_id: str):


    # =========================
    # CEK ORDER
    # =========================

    orders = order_repository.get_all()


    order = None


    for o in orders:

        if o["ref_id"] == ref_id:

            order = o

            break



    if not order:


        raise HTTPException(

            status_code=404,

            detail="Order tidak ditemukan"

        )



    # =========================
    # CREATE QRIS
    # =========================

    qris = xendit.create_qris(

        ref_id,

        order["price"]

    )



    if not qris:


        return {


            "success":False,


            "message":"Gagal membuat QRIS"


        }




    return {


        "success":True,


        "ref_id":ref_id,


        "product_name":order["product_name"],


        "price":order["price"],


        "payment":qris


    }