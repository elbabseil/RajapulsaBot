from app.pln.models import PLNTransaction


def create_pln_transaction(
    customer_id,
    customer_name,
    meter_number,
    product_name,
    amount,
    service_type
):

    return PLNTransaction(
        customer_id=customer_id,
        customer_name=customer_name,
        meter_number=meter_number,
        product_name=product_name,
        amount=amount,
        service_type=service_type
    )


def validate_customer(customer_id):

    if not customer_id:
        return False

    return True