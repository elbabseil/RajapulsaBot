from aiogram import Router, F, types

from app.services.catalog_service import catalog_service
from app.keyboards.marketplace_keyboard import build_product_keyboard


router = Router()


# ==========================================
# VOUCHER GAMES
# ==========================================

@router.message(F.text == "🎮 Voucher Game")
async def menu_game(
    message: types.Message
):

    products = catalog_service.get_products(
        "Games",
        None
    )


    if not products:

        await message.answer(
            "❌ Data Games belum tersedia"
        )

        return


    await message.answer(
        "🎮 Pilih Voucher Games",
        reply_markup=build_product_keyboard(
            products
        )
    )