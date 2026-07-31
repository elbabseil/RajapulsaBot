from app.game.game_service import validate_player


def process_game_order(data):

    valid = validate_player(
        data.get("user_id"),
        data.get("zone_id")
    )

    if not valid:
        return {
            "status": "FAILED",
            "message": "Data pemain tidak lengkap"
        }

    return {
        "status": "READY",
        "message": "Data game siap diproses"
    }