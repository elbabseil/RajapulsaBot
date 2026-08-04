from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext


from app.services.catalog_service import catalog_service
from app.services.order_service import order_service


from app.keyboards.marketplace_keyboard import (
    build_product_keyboard
)


from app.keyboards.payment_keyboard import (
    bayar_keyboard
)


from app.states.pasca import PascaState


from app.services.digiflazz_service import digiflazz


from app.database.transaction_repository import (
    transaction_repository
)



router = Router()





# =====================================================
# MENU TAGIHAN
# =====================================================

@router.message(
    F.text == "🧾 Tagihan"
)
async def menu_pascabayar(
    message: types.Message
):


    products = catalog_service.get_products(

        "Pascabayar",

        None

    )


    if not products:


        await message.answer(

            "❌ Data tagihan kosong"

        )

        return



    await message.answer(

"""
🧾 LAYANAN PASCABAYAR

Silakan pilih jenis tagihan:
""",

        reply_markup=build_product_keyboard(

            products[:30],

            "postpaid"

        )

    )






# =====================================================
# PILIH PRODUK
# =====================================================

@router.callback_query(
    F.data.startswith("postpaid:")
)
async def pilih_tagihan(

    callback: types.CallbackQuery,

    state: FSMContext

):


    sku = callback.data.replace(

        "postpaid:",

        ""

    )


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

        sku=sku,

        product_name=product.get(
            "product_name"
        )

    )



    await state.set_state(

        PascaState.waiting_customer_no

    )




    await callback.message.answer(

"""
🧾 TAGIHAN

Silakan masukkan ID Pelanggan.

Contoh:

123456789012


⚠️ Jangan masukkan nomor meter Token PLN.
"""

    )


    await callback.answer()







# =====================================================
# INQUIRY
# =====================================================

@router.message(
    PascaState.waiting_customer_no
)
async def proses_inquiry(

    message: types.Message,

    state: FSMContext

):


    customer_no = message.text.strip()



    if not customer_no.isdigit():


        await message.answer(

            "❌ ID pelanggan harus berupa angka"

        )

        return





    data = await state.get_data()



    sku = data.get(
        "sku"
    )



    if not sku:


        await message.answer(

            "❌ Produk tidak ditemukan"

        )

        await state.clear()

        return





    temp_ref = "PASCA-" + str(
        message.from_user.id
    )




    await message.answer(

        "🔎 Mengecek tagihan..."

    )





    hasil = digiflazz.inquiry_pasca(

        customer_no,

        sku,

        temp_ref

    )





    if not hasil:


        await message.answer(

            "❌ Gagal menghubungi DigiFlazz"

        )

        await state.clear()

        return






    response = hasil.get(

        "data",

        {}

    )





    nama = response.get(

        "customer_name",

        "-"

    )



    harga = int(

        response.get(

            "price",

            0

        )

    )



    admin = int(

        response.get(

            "admin",

            0

        )

    )



    total = harga + admin





    if total <= 0:


        await message.answer(

"""
❌ Tagihan tidak ditemukan.

Pastikan ID pelanggan benar.
"""

        )

        await state.clear()

        return






    # =====================================
    # CREATE ORDER
    # =====================================


    order = order_service.create_order(

        customer_no=customer_no,

        buyer_sku_code=sku,

        telegram_id=message.from_user.id

    )




    if order.get("status") == "FAILED":


        await message.answer(

            "❌ Gagal membuat transaksi"

        )

        await state.clear()

        return




    ref_id = order["ref_id"]







    transaction_repository.create(

        ref_id,

        message.chat.id,

        sku,

        nama,

        customer_no,

        total

    )







    await message.answer(

f"""
🧾 DETAIL TAGIHAN


Nama:
{nama}


Nomor:
{customer_no}


Produk:
{sku}


Tagihan:
Rp {harga:,}


Admin:
Rp {admin:,}


Total Bayar:
Rp {total:,}


🆔 ID:
{ref_id}


Silakan tekan BAYAR SEKARANG.
""",

        reply_markup=bayar_keyboard(

            ref_id

        )

    )



    await state.clear()