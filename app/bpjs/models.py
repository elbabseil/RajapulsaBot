from dataclasses import dataclass


@dataclass
class BPJSTransaction:
    va_number: str
    customer_name: str
    member_count: int
    period: str
    amount: int
    admin_fee: int
    status: str = "PENDING"
    reference: str = ""