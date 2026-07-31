from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder


router = Router()


def get_main_menu_keyboard():

    builder = ReplyKeyboardBuilder()

    builder.row(
        types.KeyboardButton(text="Pulsa Regular"),
        types.KeyboardButton(text="Paket Data")
    )

    builder.row(
        types.KeyboardButton(text="Token PLN"),
        types.KeyboardButton(text="Voucher Game")
    )

    builder.row(
        types.KeyboardButton(text="Tagihan")
    )

    builder.row(
        types.KeyboardButton(text="Riwayat Transaksi"),
        types.KeyboardButton(text="Cek Status / Bantuan")
    )

    return builder.as_markup(
        resize_keyboard=True
    )



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

    await message.answer(
        """
Selamat datang di RajaPulsa Bot

Pusat Pembelian Digital Otomatis

Layanan tersedia:

Pulsa Regular
Paket Data
Token PLN
Voucher Game
Tagihan Pascabayar

Pembayaran menggunakan QRIS otomatis.

Silahkan pilih menu.
        """,

        reply_markup=get_main_menu_keyboard()
    )