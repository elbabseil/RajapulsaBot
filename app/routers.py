from app.handlers import (
    start,
    marketplace_handler,
    product_handler,
    pln_handler,
    token_pln,
    payment_handler,
    history_handler,
    service_menu,
    ai_handler
)



def register_routers(dp):


    # =========================
    # START / MENU UTAMA
    # =========================

    dp.include_router(
        start.router
    )


    # =========================
    # SERVICE MENU
    # Prabayar / Pascabayar
    # HARUS SEBELUM AI
    # =========================

    dp.include_router(
        service_menu.router
    )


    # =========================
    # MARKETPLACE PRODUK
    # =========================

    dp.include_router(
        marketplace_handler.router
    )


    # =========================
    # PLN
    # Token PLN + Tagihan PLN
    # =========================

    dp.include_router(
        pln_handler.router
    )


    # =========================
    # TOKEN PLN
    # =========================

    dp.include_router(
        token_pln.router
    )


    # =========================
    # PEMBAYARAN QRIS
    # =========================

    dp.include_router(
        payment_handler.router
    )


    # =========================
    # RIWAYAT TRANSAKSI
    # =========================

    dp.include_router(
        history_handler.router
    )


    # =========================
    # AI ASSISTANT
    # PALING BAWAH
    # =========================

    dp.include_router(
        ai_handler.router
    )