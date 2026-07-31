from aiogram import Router, types, F

from app.database.transaction_repository import (
    transaction_repository
)


router = Router()


# =====================================
# RIWAYAT TRANSAKSI USER
# =====================================

@router.message(
    F.text == "Riwayat Transaksi"
)
async def history_menu(
    message: types.Message
):

    telegram_id = message.chat.id


    transactions = (
        transaction_repository
        .get_user_transactions(
            telegram_id,
            limit=5
        )
    )


    if not transactions:

        await message.answer(
            "📜 Belum ada riwayat transaksi."
        )

        return



    text = (
        "📜 *5 Transaksi Terakhir*\n"
        "========================\n\n"
    )


    for trx in transactions:

        text += (
            f"🆔 ID : `{trx.get('trx_id')}`\n"
            f"📦 Produk : {trx.get('product_name')}\n"
            f"🎯 Tujuan : {trx.get('customer_no')}\n"
            f"💰 Harga : Rp {trx.get('price'):,}\n"
            f"📌 Status : {trx.get('status')}\n"
            "------------------------\n"
        )


    await message.answer(
        text,
        parse_mode="Markdown"
    )