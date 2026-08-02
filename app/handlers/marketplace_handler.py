from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext


from app.services.catalog_service import catalog_service
from app.services.order_service import order_service


from app.database.transaction_repository import (
    transaction_repository
)


from app.keyboards.marketplace_keyboard import (
    build_brand_keyboard,
    build_product_keyboard
)


from app.keyboards.payment_keyboard import (
    bayar_keyboard
)


from app.states.payment import PaymentState


from app.utils.target_helper import (
    get_target_text
)



router = Router()



# ==========================================
# MENU PULSA
# ==========================================

@router.message(
    F.text == "📱 Pulsa"
)
async def menu_pulsa(
    message: types.Message
):

    brands = catalog_service.get_brands(
        "Pulsa"
    )


    if not brands:

        await message.answer(
            "❌ Operator tidak tersedia"
        )

        return



    await message.answer(

        "📱 Pilih Operator",

        reply_markup=build_brand_keyboard(
            brands
        )

    )



# ==========================================
# PILIH BRAND
# ==========================================

@router.callback_query(
    F.data.startswith("brand:")
)
async def choose_brand(
    callback: types.CallbackQuery
):


    brand = callback.data.split(":")[1]


    products = catalog_service.get_products(
        "Pulsa",
        brand
    )


    if not products:

        await callback.answer(
            "Produk tidak tersedia",
            show_alert=True
        )

        return



    await callback.message.edit_text(

        f"""
📱 {brand}

Pilih Produk
""",

        reply_markup=build_product_keyboard(
            products
        )

    )


    await callback.answer()




# ==========================================
# PILIH PRODUK
# ==========================================

@router.callback_query(
    F.data.startswith("product:")
)
async def choose_product(

    callback: types.CallbackQuery,

    state: FSMContext

):


    sku = callback.data.split(":")[1]


    product = catalog_service.get_product_by_sku(
        sku
    )



    if not product:

        await callback.answer(
            "Produk tidak ditemukan",
            show_alert=True
        )

        return




    await state.update_data(

        sku=product["buyer_sku_code"],

        product_name=product["product_name"],

        category=product["category"],

        brand=product["brand"],

        price=product["price"],

        target=None

    )



    target_text = get_target_text(
        product
    )



    # =====================================
    # PRODUK BUTUH TARGET
    # =====================================

    if target_text:


        await state.set_state(
            PaymentState.waiting_target
        )


        await callback.message.answer(

f"""
📦 Produk:
{product['product_name']}


🏷 Operator:
{product['brand']}


💰 Harga:
Rp {product['price']:,}


{target_text}
"""

        )



    # =====================================
    # PRODUK TANPA TARGET
    # CONTOH:
    # WAVE GAME
    # VOUCHER CODE
    # =====================================

    else:


        await state.clear()


        await callback.message.answer(

f"""
📦 Produk:
{product['product_name']}


🏷 Operator:
{product['brand']}


💰 Harga:
Rp {product['price']:,}


🎟 Voucher Digital


Tekan tombol BAYAR SEKARANG
untuk membuat QRIS.
""",

            reply_markup=bayar_keyboard(
                product["buyer_sku_code"]
            )

        )



    await callback.answer()




# ==========================================
# BAYAR PRODUK TANPA TARGET
# ==========================================

@router.callback_query(
    F.data.startswith("bayar:")
)
async def bayar_voucher(

    callback: types.CallbackQuery

):


    sku = callback.data.split(":")[1]



    product = catalog_service.get_product_by_sku(
        sku
    )



    if not product:

        await callback.answer(
            "Produk tidak ditemukan",
            show_alert=True
        )

        return



    await callback.message.answer(
        "⏳ Membuat order dan QRIS..."
    )



    # ===============================
    # CREATE ORDER
    # ===============================

    order = order_service.create_order(

        customer_no=None,

        buyer_sku_code=product["buyer_sku_code"],

        telegram_id=callback.from_user.id

    )



    if order.get("status") == "FAILED":


        await callback.message.answer(

            "❌ Gagal membuat order\n\n"
            +
            order.get(
                "message",
                ""
            )

        )

        return




    ref_id = order["ref_id"]




    # ===============================
    # SIMPAN TRANSAKSI
    # ===============================

    transaction_repository.create(

        ref_id,

        callback.message.chat.id,

        product["buyer_sku_code"],

        product["product_name"],

        "",

        product["price"]

    )



    # ===============================
    # BUAT QRIS
    # ===============================

    from app.services.xendit_service import xendit


    qris = xendit.create_qris(

        ref_id,

        product["price"]

    )



    if not qris:


        await callback.message.answer(

            "❌ Gagal membuat QRIS"

        )

        return




    qr_string = (

        qris.get("qr_string")

        or

        qris.get("qr_code")

    )



    transaction_repository.save_qris(

        ref_id,

        qris.get("id"),

        qr_string

    )




    qr_url = (

        "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data="

        +

        qr_string

    )




    await callback.message.answer_photo(

        qr_url,


        caption=f"""

⚡ QRIS PEMBAYARAN


📦 Produk:
{product['product_name']}


💰 Harga:
Rp {product['price']:,}


🆔 ID:
{ref_id}


Silakan lakukan pembayaran.

Setelah lunas voucher akan diproses.
"""

    )


    await callback.answer()