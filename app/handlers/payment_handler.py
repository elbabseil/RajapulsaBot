from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext


from app.states.payment import PaymentState


from app.services.product_service import get_products
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



# =================================================
# PILIH PRODUK
# =================================================

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

        if p.get(
            "buyer_sku_code"
        ) == sku:

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


    category = str(
        product.get(
            "category",
            ""
        )
    ).lower()



    product_name = product.get(
        "product_name",
        "Produk Digital"
    )



    await state.update_data(

        sku=sku,

        price=price,

        category=category,

        brand=product.get(
            "brand",
            ""
        ),

        product_name=product_name

    )




    target_text = get_target_text(
        product
    )



    # =========================================
    # PRODUK TANPA TARGET
    # =========================================

    if not target_text:


        order = order_service.create_order(

            customer_no="",

            buyer_sku_code=sku,

            telegram_id=callback.from_user.id

        )



        if order.get("status") == "FAILED":

            await callback.message.answer(
                "❌ Gagal membuat transaksi"
            )

            return



        ref_id = order["ref_id"]



        transaction_repository.create(

            ref_id,

            callback.message.chat.id,

            sku,

            product_name,

            "",

            price

        )



        await callback.message.answer(

f"""
📦 Produk:
{product_name}


💰 Harga:
Rp {price:,}


🎟 Voucher Digital


Transaksi siap.


Silakan tekan tombol pembayaran.
""",

            reply_markup=bayar_keyboard(
                ref_id
            )

        )


        await callback.answer()

        return





    # =========================================
    # PRODUK BUTUH TARGET
    # =========================================


    await state.set_state(
        PaymentState.waiting_target
    )



    await callback.message.answer(

f"""
📦 Produk:
{product_name}


🏷 Operator:
{product.get("brand","")}


💰 Harga:
Rp {price:,}


{target_text}
"""

    )


    await callback.answer()







# =================================================
# INPUT TARGET
# =================================================

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


    product_name = data.get(
        "product_name"
    )


    category = data.get(
        "category",
        ""
    )



    target = message.text.strip()




    if not target.isdigit():

        await message.answer(
            "❌ Input harus berupa angka."
        )

        return





    order = order_service.create_order(

        customer_no=target,

        buyer_sku_code=sku,

        telegram_id=message.from_user.id

    )



    if order.get("status") == "FAILED":


        await message.answer(
            "❌ Gagal membuat transaksi"
        )

        await state.clear()

        return




    ref_id = order["ref_id"]




    transaction_repository.create(

        ref_id,

        message.chat.id,

        sku,

        product_name,

        target,

        price

    )




    await message.answer(

f"""
📦 Produk:
{product_name}


🎯 Tujuan:
{target}


💰 Harga:
Rp {price:,}


✅ Transaksi dibuat.


Silakan tekan tombol pembayaran.
""",

        reply_markup=bayar_keyboard(
            ref_id
        )

    )


    await state.clear()







# =================================================
# BUTTON BAYAR SEKARANG
# =================================================

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



    if not qris:


        await callback.message.answer(
            "❌ Gagal membuat QRIS"
        )

        return




    qr_string = (

        qris.get("qr_string")

        or

        qris.get("qr_code")

        or

        qris.get("qr")

    )



    if not qr_string:


        await callback.message.answer(
            "❌ QRIS kosong"
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