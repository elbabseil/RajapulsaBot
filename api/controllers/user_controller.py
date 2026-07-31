from app.services.user_service import user_service


def register_user(
    telegram_id,
    username=None,
    full_name=None
):

    user = user_service.register(
        telegram_id,
        username,
        full_name
    )

    return {
        "success": True,
        "data": user
    }



def get_user(
    telegram_id
):

    user = user_service.get_user(
        telegram_id
    )

    if user is None:
        return {
            "success": False,
            "message": "User tidak ditemukan"
        }


    return {
        "success": True,
        "data": user
    }



def topup_user(
    telegram_id,
    amount
):

    result = user_service.topup(
        telegram_id,
        amount
    )

    return {
        "success": True,
        "data": result
    }



def purchase_user(
    telegram_id,
    amount
):

    result = user_service.purchase(
        telegram_id,
        amount
    )

    return {
        "success": True,
        "data": result
    }