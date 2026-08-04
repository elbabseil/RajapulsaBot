from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext


from app.states.payment import PaymentState


from app.services.catalog_service import catalog_service
from app.services.order_service import order_service
from app.services.xendit_service import xendit


from app.database.transaction_repository import (
    transaction_repository
)


from app.database.order_repository import (
    order_repository
)


from app.keyboards.payment_keyboard import (
    bayar_keyboard
)


from app.utils.target_helper import (
    get_target_text
)



router = Router()





# =====================================================
# PILIH PRODUK
# =====================================================

@router.callback_query(
    F.data.startswith("product:")
)
async def buy_product(
    callback: types.CallbackQuery,
    state: FSMContext
):


    parts = callback.data.split(":")


    sku = parts[-1]


    product = catalog_service.get_product_by_sku(
        sku
    )


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

        product_name=product.get(
            "product_name"
        ),

        price=price,

        category=product.get(
            "category"
        ),

        brand=product.get(
            "brand"
        )

    )



    target_text = get_target_text(product)



    if target_text:


        await state.set_state(
            PaymentState.waiting_target
        )


        await callback.message.answer(

f"""
📦 PRODUK

{product.get('product_name')}


🏷 Provider:
{product.get('brand','-')}


💰 Harga:
Rp {price:,}


{target_text}
"""

        )


        await callback.answer()

        return



    await create_transaction(

        callback,

        sku,

        "",

        product

    )


    await callback.answer()






# =====================================================
# INPUT TARGET
# =====================================================

@router.message(
    PaymentState.waiting_target
)
async def process_target(
    message: types.Message,
    state: FSMContext
):


    target = message.text.strip()



    if not target.isdigit():

        await message.answer(
            "❌ Nomor harus berupa angka"
        )

        return



    data = await state.get_data()



    sku = data.get(
        "sku"
    )



    product = catalog_service.get_product_by_sku(
        sku
    )


    if not product:

        await message.answer(
            "❌ Produk tidak ditemukan"
        )

        await state.clear()

        return



    await create_transaction(

        message,

        sku,

        target,

        product

    )



    await state.clear()





# =====================================================
# CREATE TRANSACTION
# =====================================================

async def create_transaction(
    event,
    sku,
    target,
    product
):


    order = order_service.create_order(

        customer_no=target,

        buyer_sku_code=sku,

        telegram_id=event.from_user.id

    )



    if order.get("status") == "FAILED":

        await event.message.answer(
            "❌ Gagal membuat transaksi"
        )

        return




    ref_id = order["ref_id"]



    price = int(
        product.get(
            "price",
            0
        )
    )



    transaction_repository.create(

        ref_id,

        event.message.chat.id,

        sku,

        product.get(
            "product_name"
        ),

        target,

        price

    )



    await event.message.answer(

f"""
✅ TRANSAKSI DIBUAT


📦 Produk:
{product.get('product_name')}


📱 Tujuan:
{target}


💰 Harga:
Rp {price:,}


🆔 ID:
{ref_id}


Silakan tekan BAYAR SEKARANG.
""",

        reply_markup=bayar_keyboard(
            ref_id
        )

    )








# =====================================================
# BAYAR SEKARANG
# =====================================================

@router.callback_query(
    F.data.startswith("bayar:")
)
async def create_qris(
    callback: types.CallbackQuery
):


    ref_id = callback.data.split(":")[1]



    trx = transaction_repository.get_by_trx_id(
        ref_id
    )



    if not trx:


        await callback.answer(
            "Transaksi tidak ditemukan",
            show_alert=True
        )

        return




    await callback.message.answer(
        "⏳ Membuat QRIS..."
    )




    qris = xendit.create_qris(

        ref_id,

        trx["price"]

    )



    print("==============================")
    print("XENDIT RESPONSE")
    print(qris)
    print("==============================")



    if not qris:


        await callback.message.answer(
            "❌ Xendit gagal membuat QRIS"
        )

        return





    qr_string = (

        qris.get("qr_string")

        or

        qris.get("qr_code")

        or

        qris.get("qr")

        or

        qris.get("qr_data")

    )



    if not qr_string:


        await callback.message.answer(

f"""
❌ QRIS kosong

Response Xendit:

{qris}
"""

        )

        return





    qris_id = qris.get(
        "id"
    )



    transaction_repository.update_qris(

        ref_id,

        qris_id,

        qr_string

    )



    order_repository.update_qr_id(

        ref_id,

        qris_id

    )





    qr_url = (

        "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data="

        +

        qr_string

    )




    await callback.message.answer_photo(

        qr_url,

        caption=f"""
⚡ QRIS PEMBAYARAN


📦 Produk:
{trx['product_name']}


💰 Harga:
Rp {trx['price']:,}


🆔 ID:
{ref_id}


Silakan lakukan pembayaran.
"""

    )



    await callback.answer()