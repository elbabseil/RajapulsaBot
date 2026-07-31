from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

import uuid
import json


from app.states.payment import PaymentState

from app.services.product_service import get_products
from app.services.xendit_service import xendit
from app.services.digiflazz_service import digiflazz

from app.database.transaction_repository import (
    transaction_repository
)



router = Router()



# ==========================================
# PILIH PRODUK
# ==========================================


@router.callback_query(
    F.data.startswith("buyprod_")
)
async def buy_product(

    callback: types.CallbackQuery,

    state: FSMContext

):


    data = callback.data.replace(
        "buyprod_",
        ""
    )


    sku, price = data.rsplit(
        "_",
        1
    )


    await state.update_data(

        sku=sku,

        price=int(price)

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





# ==========================================
# INPUT TARGET
# ==========================================


@router.message(
    PaymentState.waiting_target
)
async def process_target(

    message: types.Message,

    state:FSMContext

):


    data = await state.get_data()



    sku = data["sku"]

    price = data["price"]



    target = message.text.strip()



    trx_id = (

        "TRX"

        +

        uuid.uuid4()

        .hex[:10]

        .upper()

    )



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





    # SIMPAN TRANSAKSI


    transaction_repository.create(

        trx_id,

        message.chat.id,

        sku,

        product_name,

        target,

        price

    )





    await message.answer(

        "⏳ Membuat QRIS pembayaran..."

    )




    # CREATE QRIS XENDIT


    qris = xendit.create_qris(

        trx_id,

        price

    )



    if not qris:


        await message.answer(

            "❌ Gagal membuat QRIS"

        )

        return





    qr_string = (

        qris.get(

            "qr_string"

        )

        or

        qris.get(

            "qr_code"

        )

    )



    qris_id = qris.get(
        "id"
    )



    transaction_repository.save_qris(

        trx_id,

        qris_id,

        qr_string

    )





    builder = InlineKeyboardBuilder()


    builder.button(

        text="🔄 Cek Pembayaran",

        callback_data=f"check_{trx_id}_{sku}"

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

🆔 {trx_id}


Silahkan bayar QRIS.

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

    callback:types.CallbackQuery

):


    data = callback.data.replace(
        "check_",
        ""
    )


    trx_id, sku = data.split("_")



    trx = transaction_repository.get_by_trx_id(

        trx_id

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





    transaction_repository.update_status(

        trx_id,

        payment_status="PAID",

        transaction_status="PROCESSING"

    )




    await callback.message.answer(

        "✅ Pembayaran diterima.\nMengirim ke DigiFlazz..."

    )





    result = digiflazz.prepaid_transaction(

        trx["customer_no"],

        sku,

        trx_id

    )





    if result:


        transaction_repository.mark_success(

            trx_id,

            json.dumps(result)

        )


        await callback.message.answer(

            "🎉 Transaksi berhasil diproses."

        )


    else:


        transaction_repository.mark_failed(

            trx_id

        )


        await callback.message.answer(

            "❌ Transaksi gagal."

        )



    await callback.answer()