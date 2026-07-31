from fastapi import APIRouter

from api.controllers.product_controller import (
    get_all_products,
    get_prepaid_products,
    get_pasca_products,
    sync_products,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
def products():
    return get_all_products()


@router.get("/prepaid")
def prepaid():
    return get_prepaid_products()


@router.get("/pasca")
def pasca():
    return get_pasca_products()


@router.post("/sync")
def sync():
    return sync_products()