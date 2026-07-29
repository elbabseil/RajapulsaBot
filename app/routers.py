from app.handlers import start

def register_routers(dp):
    dp.include_router(start.router)