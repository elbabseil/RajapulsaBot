from fastapi import APIRouter

from api.controllers.transaction_controller import buy_product


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/buy")
def buy(
    telegram_id: str,
    buyer_sku_code: str,
    customer_no: str
):

    return buy_product(
        telegram_id,
        buyer_sku_code,
        customer_no
    )