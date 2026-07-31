from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.services.product_service import get_products


router = Router()


OPERATORS = [
    "TELKOMSEL",
    "INDOSAT",
    "XL",
    "AXIS",
    "TRI",
    "SMARTFREN",
    "BY.U"
]


# =====================================================
# MENU PULSA REGULAR
# =====================================================

@router.message(F.text == "Pulsa Regular")
async def menu_pulsa(message: types.Message):

    products = get_products()

    brands = set()


    for p in products:

        category = str(
            p.get("category", "")
        ).upper()


        brand = str(
            p.get("brand", "")
        ).upper()


        if (
            category == "PULSA"
            and brand in OPERATORS
        ):
            brands.add(brand)



    if not brands:
        await message.answer(
            "❌ Produk pulsa tidak tersedia."
        )
        return



    keyboard = InlineKeyboardBuilder()


    for brand in sorted(brands):

        keyboard.button(
            text=f"📱 {brand}",
            callback_data=f"pulsa:{brand}"
        )


    keyboard.adjust(2)



    await message.answer(
        "📱 PILIH OPERATOR PULSA",
        reply_markup=keyboard.as_markup()
    )



# =====================================================
# LIST PRODUK PULSA
# =====================================================

@router.callback_query(
    F.data.startswith("pulsa:")
)
async def pulsa_product(
    callback: types.CallbackQuery
):

    brand = callback.data.split(":")[1]


    products = get_products()


    keyboard = InlineKeyboardBuilder()


    total = 0


    for p in products:


        p_brand = str(
            p.get("brand","")
        ).upper()


        category = str(
            p.get("category","")
        ).upper()



        if (
            p_brand == brand
            and
            category == "PULSA"
        ):


            keyboard.button(

                text=(
                    f"{p.get('product_name')} "
                    f"Rp {int(p.get('price',0)):,}"
                ),

                callback_data=(
                    f"buyprod:"
                    f"{p.get('buyer_sku_code')}"
                )
            )

            total += 1



    keyboard.adjust(1)



    if total == 0:

        await callback.message.edit_text(
            "❌ Pulsa operator ini kosong."
        )

    else:

        await callback.message.edit_text(

            f"📱 PULSA {brand}\n\n"
            "Silahkan pilih nominal:",

            reply_markup=
            keyboard.as_markup()
        )



    await callback.answer()



# =====================================================
# MENU PAKET DATA
# =====================================================

@router.message(
    F.text == "Paket Data"
)
async def menu_data(
    message: types.Message
):

    products = get_products()

    brands = set()



    for p in products:


        category = str(
            p.get("category","")
        ).upper()


        brand = str(
            p.get("brand","")
        ).upper()



        name = str(
            p.get("product_name","")
        ).lower()



        if (
            category in [
                "DATA",
                "INTERNET",
                "PAKET DATA"
            ]
            or
            any(
                x in name
                for x in [
                    "data",
                    "internet",
                    "paket"
                ]
            )
        ):

            if brand in OPERATORS:

                brands.add(brand)



    keyboard = InlineKeyboardBuilder()



    for brand in sorted(brands):

        keyboard.button(

            text=f"📶 {brand}",

            callback_data=f"data:{brand}"

        )



    keyboard.adjust(2)



    await message.answer(

        "📶 PILIH OPERATOR PAKET DATA",

        reply_markup=
        keyboard.as_markup()

    )



# =====================================================
# LIST PAKET DATA
# =====================================================

@router.callback_query(
    F.data.startswith("data:")
)
async def data_product(
    callback: types.CallbackQuery
):

    brand = callback.data.split(":")[1]


    products = get_products()


    keyboard = InlineKeyboardBuilder()


    total = 0



    for p in products:


        p_brand = str(
            p.get("brand","")
        ).upper()


        name = str(
            p.get("product_name","")
        ).lower()



        if p_brand == brand:


            if any(
                x in name
                for x in [
                    "data",
                    "internet",
                    "paket"
                ]
            ):


                keyboard.button(

                    text=(

                        f"{p.get('product_name')} "
                        f"Rp {int(p.get('price',0)):,}"

                    ),

                    callback_data=(

                        f"buyprod:"
                        f"{p.get('buyer_sku_code')}"

                    )

                )


                total += 1



    keyboard.adjust(1)



    if total == 0:


        await callback.message.edit_text(
            "❌ Paket data tidak tersedia."
        )


    else:


        await callback.message.edit_text(

            f"📶 PAKET DATA {brand}\n\n"
            "Pilih paket:",

            reply_markup=
            keyboard.as_markup()

        )



    await callback.answer()