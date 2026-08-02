from fastapi import APIRouter, Query, HTTPException

from api.controllers.transaction_controller import buy_product


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/buy")
def buy(

    telegram_id: int = Query(...),

    buyer_sku_code: str = Query(...),

    customer_no: str = Query(...)

):


    print("==============================")
    print("ROUTE TRANSACTION MASUK")
    print("telegram_id:", telegram_id)
    print("sku:", buyer_sku_code)
    print("customer:", customer_no)
    print("==============================")


    try:


        result = buy_product(

            telegram_id,

            buyer_sku_code,

            customer_no

        )


        print("==============================")
        print("HASIL CONTROLLER")
        print(result)
        print("==============================")


        return result



    except Exception as e:


        import traceback

        traceback.print_exc()


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )