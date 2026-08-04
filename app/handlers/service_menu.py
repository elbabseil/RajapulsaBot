from aiogram import Router, types, F


from app.services.catalog_service import catalog_service


from app.keyboards.marketplace_keyboard import (
    build_category_keyboard,
    build_brand_keyboard,
    build_product_keyboard
)



router = Router()





# =====================================================
# MENU PREPAID
# =====================================================

@router.message(
    F.text == "⚡ Prabayar"
)
async def menu_prepaid(

    message: types.Message

):


    categories = catalog_service.get_categories(

        "prepaid"

    )



    if not categories:


        await message.answer(

            "❌ Layanan prabayar belum tersedia"

        )

        return




    await message.answer(

        """
⚡ LAYANAN PRABAYAR

Silakan pilih kategori:
""",

        reply_markup=build_category_keyboard(

            categories,

            "prepaid"

        )

    )







# =====================================================
# MENU POSTPAID
# =====================================================

@router.message(
    F.text == "🧾 Pascabayar"
)
async def menu_postpaid(

    message: types.Message

):


    categories = catalog_service.get_categories(

        "postpaid"

    )



    if not categories:


        await message.answer(

            "❌ Layanan pascabayar belum tersedia"

        )

        return




    await message.answer(

        """
🧾 LAYANAN PASCABAYAR

Silakan pilih kategori:
""",

        reply_markup=build_category_keyboard(

            categories,

            "postpaid"

        )

    )







# =====================================================
# PILIH CATEGORY
# =====================================================

@router.callback_query(
    F.data.startswith("category:")
)
async def pilih_category(

    callback: types.CallbackQuery

):


    try:


        _, service_type, category = callback.data.split(":")


    except ValueError:


        await callback.answer(

            "Format kategori salah",

            show_alert=True

        )

        return





    brands = catalog_service.get_brands(

        category,

        service_type

    )





    if not brands:


        await callback.message.answer(

            "❌ Provider tidak tersedia"

        )


        await callback.answer()

        return






    await callback.message.answer(

        f"""
🏷 PILIH PROVIDER


Kategori:
{category}

""",

        reply_markup=build_brand_keyboard(

            brands,

            service_type,

            category

        )

    )



    await callback.answer()







# =====================================================
# PILIH BRAND
# =====================================================

@router.callback_query(
    F.data.startswith("brand:")
)
async def pilih_brand(

    callback: types.CallbackQuery

):


    try:


        _, service_type, category, brand = callback.data.split(":")


    except ValueError:


        await callback.answer(

            "Format provider salah",

            show_alert=True

        )

        return






    products = catalog_service.get_products(

        category,

        brand,

        service_type

    )





    if not products:


        await callback.message.answer(

            "❌ Produk tidak ditemukan"

        )


        await callback.answer()

        return






    await callback.message.answer(

        f"""
🛒 PILIH PRODUK


Kategori:
{category}


Provider:
{brand}

""",

        reply_markup=build_product_keyboard(

            products[:50],

            service_type

        )

    )



    await callback.answer()