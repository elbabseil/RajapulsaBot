from app.handlers import (
    start,
    product_handler,
    marketplace_handler,
    payment_handler,
    history_handler,
    token_pln,
    ai_handler
)


def register_routers(dp):

    dp.include_router(
    marketplace_handler.router
  )

    dp.include_router(
        start.router
    )

    dp.include_router(
        product_handler.router
    )

    dp.include_router(
        payment_handler.router
    )

    dp.include_router(
        history_handler.router
    )

    dp.include_router(
        token_pln.router
    )

    dp.include_router(
        ai_handler.router
    )