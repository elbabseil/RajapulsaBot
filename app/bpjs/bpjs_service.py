from app.bpjs.models import BPJSTransaction


def create_bpjs_transaction(
    va_number,
    customer_name,
    member_count,
    period,
    amount,
    admin_fee
):

    return BPJSTransaction(
        va_number=va_number,
        customer_name=customer_name,
        member_count=member_count,
        period=period,
        amount=amount,
        admin_fee=admin_fee
    )


def validate_va(va_number):

    if not va_number:
        return False

    return True