from aiogram import Router
from aiogram import F
from aiogram import types

from aiogram.fsm.context import FSMContext

from app.services.catalog_service import catalog_service

from app.keyboards.marketplace_keyboard import (
    build_brand_keyboard,
    build_product_keyboard
)

router = Router()


# ==========================================
# MENU PULSA
# ==========================================

@router.message(F.text == "📱 Pulsa")
async def menu_pulsa(message: types.Message):

    brands = catalog_service.get_brands("Pulsa")

    await message.answer(

        "📱 Pilih Operator",

        reply_markup=build_brand_keyboard(
            brands
        )

    )


# ==========================================
# PILIH BRAND
# ==========================================

@router.callback_query(F.data.startswith("brand:"))
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

@router.callback_query(F.data.startswith("product:"))
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

        sku=sku,

        price=product["price"],

        product_name=product["product_name"],

        pasca=False

    )

    from app.states.form import Form

from app.states.payment import PaymentState

    await state.set_state(
        PaymentState.waiting_target
    )

    await callback.message.answer(

        f"""
📱 {product['product_name']}

Harga :

Rp {product['price']:,}

Silakan kirim nomor tujuan.
"""

    )

    await callback.answer()