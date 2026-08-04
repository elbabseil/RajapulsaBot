from aiogram import Router, types
from aiogram.filters import Command

from app.database.user_repository import user_repository


router = Router()


# =====================================
# START REGISTER USER
# =====================================

@router.message(Command("start"))
async def start_handler(
    message: types.Message
):

    user = user_repository.create_user(

        telegram_id=message.from_user.id,

        username=message.from_user.username,

        full_name=message.from_user.full_name

    )


    await message.answer(
        f"""
👋 Selamat datang di RajaPulsa

Akun Anda berhasil dibuat.

👤 Nama:
{message.from_user.full_name}

🆔 ID:
{message.from_user.id}


Silakan pilih menu:

📱 Pulsa
📶 Paket Data
⚡ Token PLN
🎮 Voucher Game
🧾 Tagihan
"""
    )