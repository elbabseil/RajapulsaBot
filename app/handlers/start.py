from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_menu_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.row(
        types.KeyboardButton(text="📱 Pulsa Regular"),
        types.KeyboardButton(text="📶 Paket Data")
    )

    builder.row(
        types.KeyboardButton(text="⚡ Token PLN"),
        types.KeyboardButton(text="🎮 Voucher Game")
    )

    builder.row(
        types.KeyboardButton(text="📋 Tagihan (Dll)")
    )

    builder.row(
        types.KeyboardButton(text="📜 Riwayat Transaksi"),
        types.KeyboardButton(text="📋 Cek Status / Bantuan")
    )

    return builder.as_markup(resize_keyboard=True)