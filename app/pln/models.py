from dataclasses import dataclass


@dataclass
class PLNTransaction:
    customer_id: str
    customer_name: str
    meter_number: str
    product_name: str
    amount: int
    service_type: str
    status: str = "PENDING"
    token: str = ""
    reference: str = ""