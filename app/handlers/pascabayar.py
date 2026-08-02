from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from app.services.catalog_service import catalog_service
from app.keyboards.marketplace_keyboard import build_product_keyboard
from app.keyboards.payment_keyboard import bayar_keyboard

from app.states.pasca import PascaState

from app.services.digiflazz_service import digiflazz
from app.services.xendit_service import xendit

from app.database.transaction_repository import transaction_repository

import uuid



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

        "🧾 Pilih Jenis Tagihan",

        reply_markup=build_product_keyboard(
            products[:30]
        )

    )




# =====================================================
# PILIH PRODUK TAGIHAN
# =====================================================

@router.callback_query(
    F.data.startswith("pasca:")
)
async def pilih_tagihan(

    callback: types.CallbackQuery,

    state: FSMContext

):


    sku = callback.data.replace(
        "pasca:",
        ""
    )


    await state.update_data(
        sku=sku
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


⚠️ Jangan masukkan nomor meter token.
"""
    )


    await callback.answer()




# =====================================================
# INQUIRY TAGIHAN
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



    ref_id = (

        "PASCA-"

        +

        str(uuid.uuid4())[:8]

    )



    await message.answer(
        "🔎 Mengecek tagihan..."
    )



    print("==============================")
    print("PLN PASCA SKU :", sku)
    print("CUSTOMER NO   :", customer_no)
    print("==============================")



    hasil = digiflazz.inquiry_pasca(

        customer_no,

        sku,

        ref_id

    )



    print("==============================")
    print("DIGIFLAZZ RESPONSE")
    print(hasil)
    print("==============================")



    if not hasil:

        await message.answer(
            "❌ Gagal menghubungi Digiflazz"
        )

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




    # ================================
    # SIMPAN TRANSAKSI
    # ================================


    transaction_repository.create(

        trx_id=ref_id,

        telegram_id=str(
            message.from_user.id
        ),

        product_code=sku,

        product_name=nama,

        customer_no=customer_no,

        price=total

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


ID:
{ref_id}

""",

reply_markup=bayar_keyboard(
    ref_id
)

    )






# =====================================================
# BUAT QRIS
# =====================================================

@router.callback_query(
    F.data.startswith("bayar:")
)
async def bayar_tagihan(

    callback: types.CallbackQuery,

    state: FSMContext

):


    trx_id = callback.data.split(":")[1]



    trx = transaction_repository.get_by_trx_id(
        trx_id
    )


    if not trx:


        await callback.message.answer(
            "❌ Transaksi tidak ditemukan"
        )

        await callback.answer()

        return




    price = trx["price"]



    await callback.message.answer(
        "💳 Membuat QRIS..."
    )



    qris = xendit.create_qris(

        trx_id,

        price

    )



    if not qris:


        await callback.message.answer(
            "❌ Gagal membuat QRIS"
        )

        await callback.answer()

        return




    transaction_repository.save_qris(

        trx_id,

        qris.get("id"),

        qris.get("qr_string")

    )



    qr_string = qris.get(
        "qr_string"
    )


    await callback.message.answer(

f"""
💳 PEMBAYARAN TAGIHAN


ID:
{trx_id}


Total:
Rp {price:,}


Silakan scan QRIS.
"""

    )


    if qr_string:

        await callback.message.answer(
            qr_string
        )



    await state.clear()

    await callback.answer()