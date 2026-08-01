from aiogram import Router, F, types

from app.services.catalog_service import catalog_service
from app.keyboards.marketplace_keyboard import build_product_keyboard


router = Router()


# ==========================================
# PASCABAYAR
# ==========================================

@router.message(F.text == "🧾 Tagihan")
async def menu_pascabayar(
    message: types.Message
):

    products = catalog_service.get_products(
        "Pascabayar",
        None
    )


    if not products:

        await message.answer(
            "❌ Data Tagihan belum tersedia"
        )

        return


    await message.answer(
        "🧾 Pilih Jenis Tagihan",
        reply_markup=build_product_keyboard(
            products
        )
    )