from aiogram import types


async def process_ai_message(
    message: types.Message
):
    """
    Handler logic AI RajaPulsa.
    Nanti bisa diganti dengan Gemini Service.
    """

    text = message.text.lower()


    if "harga" in text or "produk" in text:

        await message.answer(
            "Silakan pilih menu produk RajaPulsa untuk melihat katalog."
        )


    elif "bantuan" in text:

        await message.answer(
            """
🤖 Bantuan RajaPulsa

Layanan:
- Pulsa
- Paket Data
- Token PLN
- Voucher Game
- Tagihan

Silakan pilih menu utama.
            """
        )


    else:

        await message.answer(
            "🤖 Saya adalah asisten RajaPulsa. Ada yang bisa saya bantu?"
        )