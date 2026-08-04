from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from starlette.middleware.sessions import SessionMiddleware


# =====================================
# DATABASE
# =====================================

from app.database.product_repository import product_repository
from app.database.user_repository import user_repository
from app.database.transaction_repository import transaction_repository



# =====================================
# PUBLIC WEBSITE
# =====================================

from app.web.public_routes import router as public_router



# =====================================
# API ROUTES
# =====================================

from api.routes.product_routes import router as product_router
from api.routes.user_routes import router as user_router
from api.routes.transaction_routes import router as transaction_router

from api.controllers.payment_controller import router as payment_router
from api.controllers.auth_controller import router as auth_router

from api.routes.public_product_routes import router as public_product_router


# =====================================
# ADMIN ROUTES
# =====================================

from app.web.routes_login import router as login_router
from app.web.routes import router as admin_router
from app.web.routes_products import router as product_admin_router
from app.web.routes_transactions import router as transaction_admin_router
from app.web.routes_users import router as user_admin_router





# =====================================
# LIFESPAN
# =====================================

@asynccontextmanager
async def lifespan(app: FastAPI):


    print("==============================")
    print(" FLASH PAY RAJAPULSA START ")
    print("==============================")


    try:

        product_repository.create_table()
        user_repository.create_table()
        transaction_repository.create_table()


        print("[DATABASE] OK")


    except Exception as e:

        print(
            "[DATABASE ERROR]",
            e
        )


    yield


    print("==============================")
    print(" FLASH PAY STOP ")
    print("==============================")






# =====================================
# CREATE APP
# =====================================

app = FastAPI(

    title="FlashPay RajaPulsa",

    description="""

FlashPay RajaPulsa

Platform PPOB Digital:

- Pulsa
- Paket Data
- Token PLN
- Voucher Game
- Pascabayar
- Payment Gateway

""",

    version="1.0.0",

    lifespan=lifespan

)






# =====================================
# ERROR HANDLER
# =====================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):


    print("==============================")
    print("GLOBAL ERROR")
    print(type(exc))
    print(exc)
    print("==============================")


    return JSONResponse(

        status_code=500,

        content={

            "error": str(exc),

            "type": str(type(exc))

        }

    )






# =====================================
# SESSION
# =====================================

app.add_middleware(

    SessionMiddleware,

    secret_key="flashpay-raja-pulsa-secret-2026"

)







# =====================================
# STATIC WEBSITE
# =====================================

app.mount(

    "/static",

    StaticFiles(
        directory="app/web/static"
    ),

    name="static"

)







# =====================================
# PUBLIC WEBSITE
# =====================================

print("==============================")
print(" REGISTER PUBLIC WEBSITE ")
print("==============================")


print(
    "PUBLIC ROUTER OBJECT:",
    public_router
)


print(
    "PUBLIC ROUTER COUNT:",
    len(public_router.routes)
)


for r in public_router.routes:

    print(
        "BEFORE INCLUDE:",
        r.path
    )



# INCLUDE PUBLIC ROUTER

app.include_router(
    public_router
)



print("==============================")
print(" AFTER INCLUDE PUBLIC ")
print("==============================")


for route in app.routes:


    print(
        "TYPE:",
        type(route)
    )


    if hasattr(route, "path"):

        print(
            "PATH:",
            route.path
        )


    if hasattr(route, "original_router"):


        print(
            "INCLUDED ROUTER FOUND"
        )


        for subroute in route.original_router.routes:

            print(
                "SUB ROUTE:",
                subroute.path
            )


print("==============================")






# =====================================
# API ROUTERS
# =====================================

API_ROUTERS = [

    product_router,

    user_router,

    transaction_router,

    payment_router,

    auth_router,

    public_product_router

]



# =====================================
# PUBLIC API ROUTERS
# =====================================

from api.routes.public_order_routes import router as public_order_router


API_ROUTERS.append(
    public_order_router
)



print("==============================")
print(" REGISTER API ROUTES ")
print("==============================")


for router in API_ROUTERS:


    print(

        "API:",

        [
            route.path
            for route in router.routes
        ]

    )


    app.include_router(router)






# =====================================
# ADMIN ROUTERS
# =====================================

ADMIN_ROUTERS = [

    login_router,

    admin_router,

    product_admin_router,

    transaction_admin_router,

    user_admin_router

]


print("==============================")
print(" REGISTER ADMIN ROUTES ")
print("==============================")


for router in ADMIN_ROUTERS:


    print(

        "ADMIN:",

        [
            route.path
            for route in router.routes
        ]

    )


    app.include_router(router)




# =====================================
# BASIC API
# =====================================

@app.get("/health")
def health():

    return {

        "status": "healthy"

    }





@app.get("/api-status")
def api_status():

    return {

        "service": "FlashPay RajaPulsa API",

        "status": "online"

    }








# =====================================
# DEBUG FINAL ROUTES
# =====================================

print("==============================")
print(" FINAL REGISTERED ROUTES ")
print("==============================")


def print_routes(routes):

    for route in routes:

        if hasattr(route, "path"):

            print(
                "ROUTE:",
                route.path,
                getattr(route, "methods", None)
            )


        elif hasattr(route, "routes"):

            print_routes(
                route.routes
            )


print_routes(
    app.routes
)


print("==============================")



# TAMBAHAN DEBUG PUBLIC
print("==============================")
print("CHECK PUBLIC FINAL")
print("==============================")


for route in app.routes:

    if hasattr(route, "original_router"):

        for r in route.original_router.routes:

            print(
                "PUBLIC FINAL:",
                r.path
            )


print("==============================")