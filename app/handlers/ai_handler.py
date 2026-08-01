from aiogram import Router, types, F

from app.handlers.ai import process_ai_message


router = Router()


# ==========================================
# AI FALLBACK
# Hanya menangkap teks yang bukan menu
# ==========================================

@router.message(
    F.text
)
async def ai_handler(
    message: types.Message
):

    ignored_menu = [

        "📱 Pulsa",
        "📦 Paket Data",
        "🎮 Voucher Game",
        "⚡ Token PLN",
        "🧾 Tagihan",
        "👤 Profile",
        "📜 Riwayat"

    ]


    if message.text in ignored_menu:
        return


    await process_ai_message(
        message
    )