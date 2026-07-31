from app.game.models import GameTransaction


def create_game_transaction(
    game_name,
    product_name,
    user_id,
    zone_id,
    price
):

    transaction = GameTransaction(
        game_name=game_name,
        product_name=product_name,
        user_id=user_id,
        zone_id=zone_id,
        price=price
    )

    return transaction


def validate_player(user_id, zone_id):

    if not user_id:
        return False

    if not zone_id:
        return False

    return True