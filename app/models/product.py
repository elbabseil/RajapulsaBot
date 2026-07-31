from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    sku: str
    name: str
    category: str
    brand: str
    price: int
    selling_price: int
    active: bool = True
    created_at: datetime = datetime.now()