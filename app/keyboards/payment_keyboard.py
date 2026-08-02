from aiogram.utils.keyboard import InlineKeyboardBuilder



def bayar_keyboard(
    trx_id
):

    builder = InlineKeyboardBuilder()


    builder.button(
        text="💳 BAYAR SEKARANG",
        callback_data=f"bayar:{trx_id}"
    )


    builder.adjust(1)


    return builder.as_markup()