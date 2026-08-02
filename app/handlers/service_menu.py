from aiogram import Router, types, F

from app.services.catalog_service import catalog_service

from app.keyboards.marketplace_keyboard import (
    build_category_keyboard,
    build_brand_keyboard,
    build_product_keyboard
)


router = Router()



# ==========================================
# MENU PREPAID
# ==========================================

@router.message(
    F.text == "⚡ Prabayar"
)
async def menu_prepaid(
    message: types.Message
):


    categories = [

        "Pulsa",
        "Data",
        "Games",
        "Voucher",
        "PLN",
        "eSIM",
        "Masa Aktif"

    ]


    await message.answer(

        "⚡ Pilih Layanan Prabayar",

        reply_markup=build_category_keyboard(
            categories
        )

    )





# ==========================================
# MENU POSTPAID
# ==========================================

@router.message(
    F.text == "🧾 Pascabayar"
)
async def menu_postpaid(

    message: types.Message

):


    # Pascabayar DigiFlazz berada
    # dalam kategori Pascabayar


    brands = catalog_service.get_brands(

        "Pascabayar"

    )


    if not brands:


        await message.answer(

            "❌ Layanan Pascabayar belum tersedia"

        )

        return



    await message.answer(

        "🧾 Pilih Provider Pascabayar",

        reply_markup=build_brand_keyboard(

            brands

        )

    )





# ==========================================
# PILIH CATEGORY PREPAID
# ==========================================

@router.callback_query(
    F.data.startswith("category:")
)
async def pilih_category(

    callback: types.CallbackQuery

):


    category = callback.data.replace(

        "category:",

        ""

    )



    brands = catalog_service.get_brands(

        category

    )



    if not brands:


        await callback.message.answer(

            "❌ Provider tidak tersedia"

        )

        await callback.answer()

        return




    await callback.message.answer(

        f"📱 Pilih Provider\n\n"
        f"Layanan: {category}",


        reply_markup=build_brand_keyboard(

            brands

        )

    )


    await callback.answer()





# ==========================================
# PILIH BRAND
# ==========================================

@router.callback_query(
    F.data.startswith("brand:")
)
async def pilih_brand(

    callback: types.CallbackQuery

):


    brand = callback.data.replace(

        "brand:",

        ""

    )



    products = [

        p

        for p in catalog_service.products

        if p.get("brand") == brand

    ]



    if not products:


        await callback.message.answer(

            "❌ Produk tidak ditemukan"

        )

        await callback.answer()

        return




    await callback.message.answer(

        f"🛒 Pilih Produk\n\n"
        f"Provider: {brand}",


        reply_markup=build_product_keyboard(

            products[:30]

        )

    )


    await callback.answer()