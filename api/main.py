from fastapi import FastAPI

from api.routes.product_routes import router as product_router
from api.routes.user_routes import router as user_router
from api.routes.transaction_routes import router as transaction_router
from api.controllers.payment_controller import router as payment_router


# Database
from app.database.product_repository import product_repository
from app.database.user_repository import user_repository
from app.database.transaction_repository import transaction_repository



app = FastAPI(

    title="RajaPulsa API",

    description="""
    RajaPulsa Backend System

    Features:
    - DigiFlazz PPOB
    - Xendit QRIS Payment
    - Telegram Bot Integration
    - User Balance Management
    """,

    version="1.0.0"

)



# =================================
# STARTUP
# =================================

@app.on_event("startup")
def startup_event():

    print("==============================")
    print(" RAJAPULSA SYSTEM STARTING ")
    print("==============================")


    try:

        product_repository.create_table()

        user_repository.create_table()

        transaction_repository.create_table()


        print("[DATABASE] OK")


    except Exception as e:

        print("[DATABASE ERROR]")
        print(e)



# =================================
# ROOT
# =================================

@app.get("/")
def root():

    return {

        "status": "online",

        "service": "RajaPulsa API",

        "version": "1.0.0"

    }



@app.get("/health")
def health():

    return {

        "status": "healthy",

        "service": "RajaPulsa"

    }



# =================================
# ROUTES
# =================================


# Product
app.include_router(
    product_router
)



# User
app.include_router(
    user_router
)



# Transaction DigiFlazz
app.include_router(
    transaction_router
)



# Payment Xendit QRIS
app.include_router(
    payment_router
)