from dataclasses import dataclass


@dataclass
class GameTransaction:
    game_name: str
    product_name: str
    user_id: str
    zone_id: str
    price: int
    status: str = "PENDING"
    reference: str = ""