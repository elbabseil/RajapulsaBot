from app.handlers import (

    start,

    service_menu,

    marketplace_handler,

    token_pln,

    pascabayar,

    payment_handler,

    history_handler,

    ai_handler

)



def register_routers(dp):


    print("==============================")
    print("REGISTER ROUTERS")
    print("==============================")



    # =====================================
    # START / MENU UTAMA
    # =====================================

    dp.include_router(

        start.router

    )



    # =====================================
    # MENU LAYANAN
    # ⚡ Prabayar
    # 🧾 Pascabayar
    # =====================================

    dp.include_router(

        service_menu.router

    )



    # =====================================
    # MARKETPLACE PRODUK
    #
    # Pulsa
    # Paket Data
    # Voucher
    # Games
    # =====================================

    dp.include_router(

        marketplace_handler.router

    )



    # =====================================
    # TOKEN PLN
    # Harus sebelum payment
    # =====================================

    dp.include_router(

        token_pln.router

    )



    # =====================================
    # PASCABAYAR
    #
    # PLN Pascabayar
    # BPJS
    # PDAM
    # dll
    # =====================================

    dp.include_router(

        pascabayar.router

    )



    # =====================================
    # PAYMENT CENTER
    #
    # Semua QRIS
    # bayar:
    # =====================================

    dp.include_router(

        payment_handler.router

    )



    # =====================================
    # RIWAYAT TRANSAKSI
    # =====================================

    dp.include_router(

        history_handler.router

    )



    # =====================================
    # AI ASSISTANT
    # HARUS TERAKHIR
    # =====================================

    dp.include_router(

        ai_handler.router

    )



    print("==============================")
    print("ALL ROUTERS REGISTERED")
    print("==============================")