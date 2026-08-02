from aiogram.utils.keyboard import InlineKeyboardBuilder



def build_category_keyboard(categories):

    builder = InlineKeyboardBuilder()


    for category in categories:

        builder.button(
            text=category,
            callback_data=f"category:{category}"
        )


    builder.adjust(2)


    return builder.as_markup()




def build_brand_keyboard(brands):

    builder = InlineKeyboardBuilder()


    for brand in brands:

        builder.button(
            text=brand,
            callback_data=f"brand:{brand}"
        )


    builder.adjust(2)


    return builder.as_markup()