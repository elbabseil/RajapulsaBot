from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext


from app.states.token_pln_state import TokenPLNState


from app.services.catalog_service import catalog_service
from app.services.order_service import order_service


from app.database.transaction_repository import (
    transaction_repository
)


from app.keyboards.payment_keyboard import (
    bayar_keyboard
)



router = Router()





# =====================================================
# MENU TOKEN PLN
# =====================================================

@router.message(
    F.text == "Token PLN"
)
async def token_pln_menu(
    message: types.Message
):


    await message.answer(
"""
⚡ TOKEN PLN


Silakan pilih nominal:


20.000

50.000

100.000

200.000

1.000.000

"""
    )


    await message.answer(
        "Silakan pilih nominal token PLN."
    )





# =====================================================
# PILIH NOMINAL TOKEN PLN
# =====================================================

@router.message(
    F.text.in_(
        [
            "20.000",
            "50.000",
            "100.000",
            "200.000",
            "1.000.000",

            "20000",
            "50000",
            "100000",
            "200000",
            "1000000"
        ]
    )
)
async def token_pln_nominal(

    message: types.Message,

    state: FSMContext

):


    mapping = {


        "20.000": "pln20",
        "20000": "pln20",


        "50.000": "pln50",
        "50000": "pln50",


        "100.000": "pln100",
        "100000": "pln100",


        "200.000": "pln200",
        "200000": "pln200",


        "1.000.000": "pln1000",
        "1000000": "pln1000"

    }



    sku = mapping.get(
        message.text
    )



    product = catalog_service.get_product_by_sku(
        sku
    )



    if not product:


        await message.answer(

            "❌ Produk Token PLN tidak ditemukan"

        )

        return






    price = int(

        product.get(

            "price",

            0

        )

    )





    await state.update_data(

        sku=product["buyer_sku_code"],

        product_name=product["product_name"],

        price=price

    )





    await state.set_state(

        TokenPLNState.waiting_meter

    )






    await message.answer(

f"""
⚡ TOKEN PLN


Produk:

{product['product_name']}


💰 Harga:

Rp {price:,}



Silakan masukkan nomor meter PLN.
"""

    )







# =====================================================
# INPUT NOMOR METER PLN
# =====================================================

@router.message(
    TokenPLNState.waiting_meter
)
async def proses_meter_pln(

    message: types.Message,

    state: FSMContext

):


    meter = message.text.strip()



    if not meter.isdigit():


        await message.answer(

            "❌ Nomor meter harus berupa angka"

        )

        return






    data = await state.get_data()



    sku = data.get(
        "sku"
    )


    product_name = data.get(
        "product_name"
    )


    price = data.get(
        "price"
    )






    if not sku:


        await message.answer(

            "❌ Produk Token PLN tidak ditemukan"

        )


        await state.clear()

        return







    # =====================================
    # CREATE ORDER
    # =====================================


    order = order_service.create_order(

        customer_no=meter,

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







    # =====================================
    # SIMPAN TRANSAKSI
    # =====================================


    transaction_repository.create(

        ref_id,

        message.chat.id,

        sku,

        product_name,

        meter,

        price

    )







    await message.answer(

f"""
✅ TRANSAKSI DIBUAT


⚡ Produk:

{product_name}


🔢 Nomor Meter:

{meter}


💰 Harga:

Rp {price:,}


🆔 ID:

{ref_id}



Silakan tekan tombol BAYAR SEKARANG.
""",

        reply_markup=bayar_keyboard(

            ref_id

        )

    )





    await state.clear()