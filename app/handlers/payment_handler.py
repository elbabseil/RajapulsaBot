from aiogram import Router, types, F

from aiogram.fsm.context import FSMContext

from aiogram.utils.keyboard import InlineKeyboardBuilder

import json


from app.states.payment import PaymentState


from app.services.product_service import get_products
from app.services.xendit_service import xendit
from app.services.digiflazz_service import digiflazz
from app.services.order_service import order_service


from app.database.transaction_repository import (
    transaction_repository
)


from app.database.order_repository import (
    order_repository
)



router = Router()



# ==========================================
# PILIH PRODUK
# ==========================================

@router.callback_query(
    F.data.startswith("product:")
)
async def buy_product(

    callback: types.CallbackQuery,

    state: FSMContext

):


    sku = callback.data.replace(
        "product:",
        ""
    )


    products = get_products()

    product = None


    for p in products:

        if p.get("buyer_sku_code") == sku:

            product = p

            break



    if not product:

        await callback.answer(

            "Produk tidak ditemukan",

            show_alert=True

        )

        return



    price = int(

        product.get(
            "price",
            0
        )

    )


    await state.update_data(

        sku=sku,

        price=price

    )


    await state.set_state(

        PaymentState.waiting_target

    )


    await callback.message.answer(

        """
🆔 Masukkan nomor tujuan:

Contoh:

08123456789

ID pelanggan PLN
        """

    )


    await callback.answer()


    await callback.answer()





# ==========================================
# INPUT TARGET
# ==========================================

@router.message(
    PaymentState.waiting_target
)
async def process_target(

    message: types.Message,

    state: FSMContext

):


    data = await state.get_data()



    sku = data.get(
        "sku"
    )


    price = data.get(
        "price"
    )



    if not sku or not price:


        await message.answer(

            "❌ Data produk tidak ditemukan."

        )


        await state.clear()

        return




    target = message.text.strip()



    # =========================
    # CREATE ORDER RAJAPULSA
    # =========================

    order = order_service.create_order(

        customer_no=target,

        buyer_sku_code=sku,

        telegram_id=message.from_user.id

    )



    if order.get("status") == "FAILED":


        await message.answer(

            "❌ Gagal membuat order\n\n"
            +
            order.get("message")

        )


        await state.clear()

        return




    ref_id = order["ref_id"]




    # =========================
    # AMBIL PRODUK
    # =========================

    products = get_products()


    product_name = "Produk Digital"



    for p in products:


        if p.get(
            "buyer_sku_code"
        ) == sku:


            product_name = p.get(
                "product_name"
            )

            break





    # =========================
    # SIMPAN TRANSAKSI
    # =========================


    transaction_repository.create(

        ref_id,

        message.chat.id,

        sku,

        product_name,

        target,

        price

    )





    await message.answer(

        "⏳ Membuat QRIS pembayaran..."

    )





    # =========================
    # CREATE QRIS
    # =========================

    qris = xendit.create_qris(

        ref_id,

        price

    )


    print("==============================")
    print("[DEBUG QRIS DATA]")
    print(qris)
    print("==============================")


    if not qris:

        await message.answer(

            "❌ Gagal membuat QRIS"

        )

        await state.clear()

        return




    # =========================
    # QR STRING
    # =========================

    qr_string = (

        qris.get("qr_string")

        or

        qris.get("qr_code")

        or

        qris.get("qr")

    )


    if not qr_string:

        await message.answer(

            "❌ QRIS tidak tersedia"

        )

        await state.clear()

        return




    # =========================
    # SIMPAN QRIS
    # =========================


    qris_id = qris.get(
        "id"
    )


    print(
        "[DEBUG QR ID]",
        qris_id
    )


    transaction_repository.save_qris(

        ref_id,

        qris_id,

        qr_string

    )


    order_repository.update_qr_id(

        ref_id,

        qris_id

    )
    # =========================
    # BUTTON CEK
    # =========================

    builder = InlineKeyboardBuilder()



    builder.button(

        text="🔄 Cek Pembayaran",

        callback_data=f"check_{ref_id}_{sku}"

    )



    builder.adjust(1)





    qr_url = (

        "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data="

        +

        qr_string

    )





    await message.answer_photo(

        qr_url,

        caption=f"""

⚡ *QRIS PEMBAYARAN*

📦 {product_name}

🎯 {target}

💰 Rp {price:,}

🆔 {ref_id}


Silakan bayar QRIS.

        """,

        parse_mode="Markdown",

        reply_markup=builder.as_markup()

    )



    await state.clear()






# ==========================================
# CEK PEMBAYARAN
# ==========================================


@router.callback_query(

    F.data.startswith("check_")

)
async def check_payment(

    callback: types.CallbackQuery

):


    data = callback.data.replace(

        "check_",

        ""

    )



    ref_id, sku = data.split("_")





    trx = transaction_repository.get_by_trx_id(

        ref_id

    )



    if not trx:


        await callback.answer(

            "Transaksi tidak ditemukan",

            show_alert=True

        )

        return





    status = xendit.get_qris_status(

        trx["qris_id"]

    )



    if not status:


        await callback.answer(

            "Gagal cek pembayaran",

            show_alert=True

        )

        return





    payment_status = str(

        status.get(

            "status",

            ""

        )

    ).upper()





    if payment_status not in [

        "COMPLETED",
        "PAID",
        "SUCCESS"

    ]:

        await callback.answer(

            "Pembayaran belum masuk",

            show_alert=True

        )

        return



    # =========================
    # UPDATE PAYMENT STATUS ORDER
    # =========================

    order_repository.update_payment_status(

        ref_id,

        "PAID"

    )



    await callback.message.answer(

        "✅ Pembayaran diterima.\n"
        "⏳ Transaksi sedang diproses oleh sistem..."

    )


    await callback.answer()