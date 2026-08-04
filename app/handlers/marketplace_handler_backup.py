from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext


from app.states.payment import PaymentState


from app.services.catalog_service import catalog_service
from app.services.order_service import order_service


from app.database.transaction_repository import (
    transaction_repository
)


from app.keyboards.payment_keyboard import (
    bayar_keyboard
)


from app.utils.target_helper import (
    get_target_text
)



router = Router()



# =====================================================
# PILIH PRODUK PREPAID
# =====================================================

@router.callback_query(
    F.data.startswith("prepaid:")
)
async def pilih_produk_prepaid(
    callback: types.CallbackQuery,
    state: FSMContext
):


    sku = callback.data.split(":")[1]


    await proses_produk(
        callback,
        state,
        sku
    )


    await callback.answer()



# =====================================================
# PILIH PRODUK POSTPAID
# =====================================================

@router.callback_query(
    F.data.startswith("postpaid:")
)
async def pilih_produk_postpaid(
    callback: types.CallbackQuery,
    state: FSMContext
):


    sku = callback.data.split(":")[1]


    await proses_produk(
        callback,
        state,
        sku
    )


    await callback.answer()




# =====================================================
# PROSES PRODUK
# =====================================================

async def proses_produk(
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



    await state.update_data(

        sku=sku,

        product_name=product.get(
            "product_name"
        ),

        category=product.get(
            "category"
        ),

        brand=product.get(
            "brand"
        ),

        price=price

    )



    target_text = get_target_text(
        product
    )



    # produk membutuhkan nomor

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




    # produk tanpa target

    await create_order(

        callback,

        sku,

        "",

        product

    )






# =====================================================
# INPUT TARGET
# =====================================================

@router.message(
    PaymentState.waiting_target
)
async def input_target(

    message: types.Message,

    state:FSMContext

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




    await create_order(

        message,

        sku,

        target,

        product

    )



    await state.clear()







# =====================================================
# CREATE ORDER
# =====================================================

async def create_order(

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


🏷 Provider:
{product.get('brand','-')}


💰 Harga:
Rp {price:,}


ID:
{ref_id}


Silakan tekan BAYAR SEKARANG.
""",

        reply_markup=bayar_keyboard(
            ref_id
        )

    )