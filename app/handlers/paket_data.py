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
            p.get("brand", "")
        ).upper()


        category = str(
            p.get("category", "")
        ).upper()


        product_name = str(
            p.get("product_name", "")
        ).lower()



        if (
            p_brand == brand
            and
            (
                category in [
                    "DATA",
                    "INTERNET",
                    "PAKET DATA"
                ]
                or
                any(
                    x in product_name
                    for x in [
                        "data",
                        "internet",
                        "paket"
                    ]
                )
            )
        ):


            keyboard.button(

                text=(

                    f"{p.get('product_name')} "
                    f"Rp {int(p.get('price',0)):,}"

                ),

                callback_data=(

                    f"product:"
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
            "Silahkan pilih paket:",

            reply_markup=
            keyboard.as_markup()

        )


    await callback.answer()