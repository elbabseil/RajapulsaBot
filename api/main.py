from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware


# =====================================
# DATABASE
# =====================================

from app.database.product_repository import product_repository
from app.database.user_repository import user_repository
from app.database.transaction_repository import transaction_repository



# =====================================
# API ROUTERS
# =====================================

from api.routes.product_routes import router as product_router
from api.routes.user_routes import router as user_router
from api.routes.transaction_routes import router as transaction_router
from api.controllers.payment_controller import router as payment_router
from api.controllers.auth_controller import router as auth_router



# =====================================
# ADMIN ROUTERS
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


    product_repository.create_table()
    user_repository.create_table()
    transaction_repository.create_table()


    print("[DATABASE] OK")


    yield


    print("==============================")
    print(" FLASH PAY STOP ")
    print("==============================")



# =====================================
# CREATE APP
# =====================================

app = FastAPI(

    title="FlashPay RajaPulsa",

    version="1.0.0",

    lifespan=lifespan

)

from fastapi import Request
from fastapi.responses import JSONResponse


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
# SESSION ADMIN
# =====================================

app.add_middleware(

    SessionMiddleware,

    secret_key="flashpay-raja-pulsa-secret-2026"

)



# =====================================
# STATIC FILE
# =====================================

app.mount(

    "/static",

    StaticFiles(
        directory="app/web/static"
    ),

    name="static"

)



# =====================================
# BASIC ROUTES
# =====================================

@app.get("/")
def root():

    return {

        "service": "FlashPay RajaPulsa",

        "status": "online"

    }



@app.get("/health")
def health():

    return {

        "status": "healthy"

    }



# =====================================
# REGISTER API ROUTES
# =====================================

API_ROUTERS = [

    product_router,
    user_router,
    transaction_router,
    payment_router,
    auth_router

]


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
# REGISTER ADMIN ROUTES
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
# ROUTE CHECK
# =====================================

print("==============================")
print(" REGISTERED ROUTES ")
print("==============================")


for route in app.routes:

    # normal route
    if hasattr(route, "path"):

        print(
            route.path,
            getattr(route, "methods", None)
        )


    # included router
    elif hasattr(route, "original_router"):

        print(
            "INCLUDED ROUTER"
        )

        for subroute in route.original_router.routes:

            print(
                subroute.path,
                getattr(
                    subroute,
                    "methods",
                    None
                )
            )


print("==============================")