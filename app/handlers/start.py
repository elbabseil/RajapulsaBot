from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.database.user_repository import user_repository


router = Router()


# ==========================================
# MAIN MENU KEYBOARD
# ==========================================

def get_main_menu_keyboard():

    builder = ReplyKeyboardBuilder()


    builder.row(

        types.KeyboardButton(
            text="⚡ Prabayar"
        ),

        types.KeyboardButton(
            text="🧾 Pascabayar"
        )

    )


    builder.row(

        types.KeyboardButton(
            text="Riwayat Transaksi"
        ),

        types.KeyboardButton(
            text="Cek Status / Bantuan"
        )

    )


    return builder.as_markup(
        resize_keyboard=True
    )



# ==========================================
# START COMMAND + REGISTER USER
# ==========================================

@router.message(
    Command(
        commands=[
            "start",
            "menu"
        ]
    )
)
async def start_command(
    message: types.Message
):


    # ======================================
    # REGISTER USER OTOMATIS
    # ======================================

    user_repository.create_user(

        telegram_id=message.from_user.id,

        username=message.from_user.username,

        full_name=message.from_user.full_name

    )



    await message.answer(

        """
🤖 Selamat datang di RajaPulsa Bot


Pusat Pembelian Digital Otomatis


Silakan pilih jenis layanan:


⚡ Prabayar

Pulsa, Data, Game, Voucher, PLN Token


🧾 Pascabayar

PLN Pascabayar, Gas, TV


💳 Pembayaran menggunakan QRIS otomatis.
""",

        reply_markup=get_main_menu_keyboard()

    )