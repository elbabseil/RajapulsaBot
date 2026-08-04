from aiogram.utils.keyboard import InlineKeyboardBuilder



# ==========================================
# CATEGORY
# ==========================================

def build_category_keyboard(
    categories,
    product_type="prepaid"
):

    builder = InlineKeyboardBuilder()


    for category in categories:

        builder.button(

            text=category,

            callback_data=(
                f"category:{product_type}:{category}"
            )

        )


    builder.adjust(2)

    return builder.as_markup()




# ==========================================
# BRAND
# ==========================================

def build_brand_keyboard(
    brands,
    product_type,
    category
):

    builder = InlineKeyboardBuilder()


    for brand in brands:

        builder.button(

            text=brand,

            callback_data=(
                f"brand:{product_type}:{category}:{brand}"
            )

        )


    builder.adjust(2)

    return builder.as_markup()




# ==========================================
# PRODUCT
# ==========================================

def build_product_keyboard(
    products,
    product_type="prepaid"
):


    builder = InlineKeyboardBuilder()



    for product in products:


        sku = product.get(
            "buyer_sku_code"
        )


        if not sku:
            continue



        name = product.get(
            "product_name",
            "Produk"
        )


        price = int(
            product.get(
                "price",
                0
            )
        )



        if product_type == "postpaid":


            text = name


            callback = (
                f"postpaid:{sku}"
            )


        else:


            text = name


            if price:

                text += (
                    f"\nRp {price:,}"
                )


            callback = (
                f"prepaid:{sku}"
            )



        builder.button(

            text=text,

            callback_data=callback

        )



    builder.adjust(1)


    return builder.as_markup()