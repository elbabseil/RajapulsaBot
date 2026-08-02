from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from app.states.payment import PaymentState
from app.services.product_service import get_products


router = Router()


PLN_SKU = {

    "20.000": "pln20",

    "50.000": "pln50",

    "100.000": "pln100",

    "1.000.000": "pln1000",

    # format tanpa titik
    "20000": "pln20",

    "50000": "pln50",

    "100000": "pln100",

    "1000000": "pln1000"

}



@router.message(
    F.text == "Token PLN"
)
async def token_pln_menu(
    message: types.Message
):

    await message.answer(
        """
⚡ Token PLN

Silakan pilih nominal:

20.000
50.000
100.000
1.000.000
"""
    )



@router.message(
    F.text.in_(
        list(PLN_SKU.keys())
    )
)
async def token_pln_nominal(
    message: types.Message,
    state: FSMContext
):


    sku = PLN_SKU.get(
        message.text
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

        await message.answer(
            "❌ Produk PLN tidak ditemukan"
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



    await message.answer(
        f"""
⚡ Token PLN

Produk:
{product.get('product_name')}

Harga:
Rp {price:,}

Silakan masukkan nomor meter PLN.
"""
    )