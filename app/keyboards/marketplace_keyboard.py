from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_brand_keyboard(brands):

    builder = InlineKeyboardBuilder()

    for brand in brands:

        builder.button(
            text=brand,
            callback_data=f"brand:{brand}"
        )

    builder.adjust(2)

    return builder.as_markup()



def build_product_keyboard(products):

    builder = InlineKeyboardBuilder()

    for p in products:

        builder.button(

            text=f"{p['product_name']}  |  Rp {p['price']:,}",

            callback_data=f"product:{p['buyer_sku_code']}"

        )

    builder.adjust(1)

    return builder.as_markup()