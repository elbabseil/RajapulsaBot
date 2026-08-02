from aiogram.utils.keyboard import InlineKeyboardBuilder



# ==========================================
# CATEGORY KEYBOARD
# ==========================================

def build_category_keyboard(categories):

    builder = InlineKeyboardBuilder()


    for category in categories:

        builder.button(

            text=category,

            callback_data=f"category:{category}"

        )


    builder.adjust(2)


    return builder.as_markup()





# ==========================================
# BRAND KEYBOARD
# ==========================================

def build_brand_keyboard(brands):

    builder = InlineKeyboardBuilder()


    for brand in brands:

        builder.button(

            text=brand,

            callback_data=f"brand:{brand}"

        )


    builder.adjust(2)


    return builder.as_markup()





# ==========================================
# PRODUCT KEYBOARD
# PREPAID + POSTPAID
# ==========================================

def build_product_keyboard(products):

    builder = InlineKeyboardBuilder()



    for p in products:


        sku = p.get(
            "buyer_sku_code"
        )


        if not sku:
            continue



        product_name = p.get(

            "product_name",

            "Produk"

        )



        service_type = str(

            p.get(
                "service_type",
                ""
            )

        ).upper()



        price = int(

            p.get(
                "price",
                0
            )

        )



        # ==================================
        # POSTPAID
        # ==================================

        if service_type == "POSTPAID":


            text = product_name



        # ==================================
        # PREPAID
        # ==================================

        else:


            text = product_name


            if price > 0:

                text += (
                    f" | Rp {price:,}"
                )



        builder.button(

            text=text,

            callback_data=f"product:{sku}"

        )



    builder.adjust(1)


    return builder.as_markup()