from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from app.services.catalog_service import catalog_service

from app.keyboards.marketplace_keyboard import (
    build_brand_keyboard,
    build_product_keyboard
)

from app.states.payment import PaymentState


router = Router()


# ==========================================
# MENU PULSA
# ==========================================

@router.message(F.text == "📱 Pulsa")
async def menu_pulsa(
    message: types.Message
):

    brands = catalog_service.get_brands(
        "Pulsa"
    )


    if not brands:
        await message.answer(
            "❌ Operator tidak tersedia"
        )
        return


    await message.answer(
        "📱 Pilih Operator",
        reply_markup=build_brand_keyboard(
            brands
        )
    )



# ==========================================
# PILIH BRAND
# ==========================================

@router.callback_query(
    F.data.startswith("brand:")
)
async def choose_brand(
    callback: types.CallbackQuery,
    state: FSMContext
):

    brand = callback.data.split(":")[1]


    await state.update_data(
        category="Pulsa",
        brand=brand
    )


    products = catalog_service.get_products(
        "Pulsa",
        brand
    )


    if not products:

        await callback.answer(
            "Produk tidak tersedia",
            show_alert=True
        )

        return


    await callback.message.edit_text(
        f"📱 {brand}\n\nPilih Nominal",
        reply_markup=build_product_keyboard(
            products
        )
    )


    await callback.answer()



# ==========================================
# PILIH PRODUK
# ==========================================

@router.callback_query(
    F.data.startswith("product:")
)
async def choose_product(
    callback: types.CallbackQuery,
    state: FSMContext
):

    sku = callback.data.split(":")[1]


    product = catalog_service.get_product_by_sku(
        sku
    )


    if not product:

        await callback.answer(
            "Produk tidak ditemukan",
            show_alert=True
        )

        return



    await state.update_data(

        sku=product["buyer_sku_code"],

        product_id=product["id"],

        product_name=product["product_name"],

        category=product["category"],

        brand=product["brand"],

        price=product["price"]

    )


    await state.set_state(
        PaymentState.waiting_target
    )


    await callback.message.answer(
        f"""
📱 Produk:
{product['product_name']}

🏷 Operator:
{product['brand']}

💰 Harga:
Rp {product['price']:,}

Silakan kirim nomor tujuan.
"""
    )


    await callback.answer()