from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext


from app.services.catalog_service import catalog_service
from app.services.order_service import order_service


from app.database.transaction_repository import (
    transaction_repository
)


from app.keyboards.payment_keyboard import (
    bayar_keyboard
)


from app.states.payment import PaymentState


from app.utils.target_helper import (
    get_target_text
)



router = Router()





# =====================================================
# PREPAID PRODUCT
# =====================================================

@router.callback_query(
    F.data.startswith("prepaid:")
)
async def choose_prepaid(
    callback: types.CallbackQuery,
    state: FSMContext
):

    sku = callback.data.split(":")[1]

    await process_product(
        callback,
        state,
        sku
    )

    await callback.answer()





# =====================================================
# POSTPAID PRODUCT
# =====================================================

@router.callback_query(
    F.data.startswith("postpaid:")
)
async def choose_postpaid(
    callback: types.CallbackQuery,
    state: FSMContext
):

    sku = callback.data.split(":")[1]

    await process_product(
        callback,
        state,
        sku
    )

    await callback.answer()





# =====================================================
# PROCESS PRODUCT
# =====================================================

async def process_product(
    callback,
    state,
    sku
):


    product = catalog_service.get_product_by_sku(
        sku
    )


    if not product:

        await callback.message.answer(
            "❌ Produk tidak ditemukan"
        )

        return



    price = int(
        product.get(
            "price",
            0
        )
    )



    target_text = get_target_text(
        product
    )



    await state.update_data(

        sku=sku,

        product_name=product.get(
            "product_name"
        ),

        brand=product.get(
            "brand",
            "-"
        ),

        category=product.get(
            "category",
            ""
        ),

        price=price

    )





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

        return






    # produk tanpa nomor langsung buat transaksi


    await create_transaction(
        callback.message,
        callback.from_user.id,
        state
    )








# =====================================================
# INPUT TARGET
# =====================================================

@router.message(
    PaymentState.waiting_target
)
async def receive_target(

    message: types.Message,

    state: FSMContext

):


    target = message.text.strip()



    if not target.isdigit():

        await message.answer(
            "❌ Nomor harus berupa angka"
        )

        return




    await state.update_data(
        target=target
    )



    await create_transaction(

        message,

        message.from_user.id,

        state

    )





# =====================================================
# CREATE TRANSACTION
# QRIS TIDAK DISINI
# HANYA BUAT ORDER
# =====================================================

async def create_transaction(

    message,

    telegram_id,

    state

):


    data = await state.get_data()



    sku = data.get(
        "sku"
    )


    product_name = data.get(
        "product_name"
    )


    price = int(
        data.get(
            "price",
            0
        )
    )


    target = data.get(
        "target",
        ""
    )





    order = order_service.create_order(

        customer_no=target,

        buyer_sku_code=sku,

        telegram_id=telegram_id

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
✅ TRANSAKSI DIBUAT


📦 Produk:
{product_name}


📱 Tujuan:
{target if target else "-"}


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



    await state.clear()