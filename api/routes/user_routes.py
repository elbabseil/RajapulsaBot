from fastapi import APIRouter

from api.controllers.user_controller import (
    register_user,
    get_user,
    topup_user,
    purchase_user
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@router.post("/register")
def register(
    telegram_id: str,
    username: str = None,
    full_name: str = None
):

    return register_user(
        telegram_id,
        username,
        full_name
    )



@router.get("/{telegram_id}")
def detail(
    telegram_id: str
):

    return get_user(
        telegram_id
    )



@router.post("/topup")
def topup(
    telegram_id: str,
    amount: int
):

    return topup_user(
        telegram_id,
        amount
    )



@router.post("/purchase")
def purchase(
    telegram_id: str,
    amount: int
):

    return purchase_user(
        telegram_id,
        amount
    )