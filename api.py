from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


from app.services.product_service import get_products
from app.services.digiflazz_service import digiflazz
from app.services.order_service import order_service
from app.database.order_repository import order_repository



app = FastAPI(
    title="RajaPulsaBot API",
    description="API Management RajaPulsaBot",
    version="1.0.0"
)



# =========================
# HOME
# =========================

@app.get("/")
async def home():

    return {
        "project": "RajaPulsaBot",
        "status": "running"
    }



# =========================
# HEALTH
# =========================

@app.get("/health")
async def health():

    return {
        "status": "OK"
    }



# =========================
# INFO
# =========================

@app.get("/api/info")
async def info():

    return {
        "name": "RajaPulsaBot",
        "version": "1.0"
    }



# =========================
# PRODUCT API
# =========================

@app.get("/api/products")
async def products():

    data = get_products()

    return {
        "total": len(data),
        "products": data
    }



# =========================
# PRODUCT DETAIL
# =========================

@app.get("/api/products/{sku}")
async def product_detail(sku: str):

    products = get_products()


    for product in products:

        if product["buyer_sku_code"] == sku:

            return product


    raise HTTPException(
        status_code=404,
        detail="Produk tidak ditemukan"
    )



# =========================
# BALANCE API
# =========================

@app.get("/api/balance")
async def balance():

    result = digiflazz.check_balance()

    return result



# =========================
# ORDER MODEL
# =========================

class OrderRequest(BaseModel):

    customer_no: str

    buyer_sku_code: str



# =========================
# CREATE ORDER
# =========================

@app.post("/api/order")
async def order(request: OrderRequest):

    result = order_service.create_order(

        customer_no=request.customer_no,

        buyer_sku_code=request.buyer_sku_code

    )


    return result



# =========================
# ORDER HISTORY
# =========================

@app.get("/api/orders")
async def orders():

    return order_repository.get_all()



# =========================
# ORDER DETAIL
# =========================

@app.get("/api/orders/{ref_id}")
async def order_detail(ref_id: str):

    data = order_repository.get_by_ref(ref_id)


    if not data:

        raise HTTPException(
            status_code=404,
            detail="Order tidak ditemukan"
        )


    return data