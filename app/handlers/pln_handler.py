from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import uuid


from app.services.order_service import order_service
from app.services.xendit_service import xendit
from app.services.digiflazz_service import digiflazz

from app.database.order_repository import order_repository



router = Router()



class PLNState(StatesGroup):

    waiting_meter = State()

    waiting_customer_number = State()





# =====================================================
# MENU PLN
# =====================================================

@router.message(
    F.text == "⚡ PLN"
)
async def pln_menu(
    message: types.Message
):


    builder = InlineKeyboardBuilder()


    builder.button(
        text="🔋 Token PLN Prabayar",
        callback_data="pln_token"
    )


    builder.button(
        text="🧾 Tagihan PLN Pascabayar",
        callback_data="pln_tagihan"
    )


    builder.adjust(1)



    await message.answer(

        """
⚡ Layanan PLN

Silakan pilih layanan:
""",

        reply_markup=builder.as_markup()

    )





# =====================================================
# TOKEN PLN MENU
# =====================================================

@router.callback_query(
    F.data == "pln_token"
)
async def token_menu(
    callback: types.CallbackQuery
):


    builder = InlineKeyboardBuilder()



    produk = [

        ("Rp 20.000","pln20"),

        ("Rp 50.000","pln50"),

        ("Rp 100.000","pln100"),

        ("Rp 1.000.000","pln1000")

    ]



    for nama,sku in produk:


        builder.button(

            text=nama,

            callback_data=f"token:{sku}"

        )



    builder.adjust(2)



    await callback.message.answer(

        """
🔋 Token PLN Prabayar

Pilih nominal:
""",

        reply_markup=builder.as_markup()

    )



    await callback.answer()






# =====================================================
# PILIH TOKEN
# =====================================================

@router.callback_query(
    F.data.startswith("token:")
)
async def pilih_token(

    callback: types.CallbackQuery,

    state:FSMContext

):


    sku = callback.data.replace(
        "token:",
        ""
    )



    await state.update_data(
        sku=sku
    )



    await state.set_state(
        PLNState.waiting_meter
    )



    await callback.message.answer(

        """
🔋 Token PLN

Masukkan nomor meter PLN:
"""

    )



    await callback.answer()







# =====================================================
# PROSES TOKEN PLN
# =====================================================

@router.message(
    PLNState.waiting_meter
)
async def proses_token(

    message:types.Message,

    state:FSMContext

):


    data = await state.get_data()


    sku=data.get(
        "sku"
    )


    meter=message.text.strip()



    order = order_service.create_order(

        customer_no=meter,

        buyer_sku_code=sku,

        telegram_id=message.from_user.id

    )



    if order["status"]=="FAILED":


        await message.answer(

            "❌ Produk PLN tidak ditemukan"

        )

        await state.clear()

        return



    await buat_qris(

        message,

        order

    )



    await state.clear()








# =====================================================
# TAGIHAN PLN PASCABAYAR
# =====================================================

@router.callback_query(
    F.data=="pln_tagihan"
)
async def menu_tagihan(

    callback:types.CallbackQuery,

    state:FSMContext

):


    await state.set_state(

        PLNState.waiting_customer_number

    )



    await callback.message.answer(

        """
🧾 Tagihan PLN Pascabayar

Masukkan nomor pelanggan PLN:
"""

    )



    await callback.answer()






# =====================================================
# INQUIRY TAGIHAN PLN
# =====================================================

@router.message(
    PLNState.waiting_customer_number
)
async def proses_tagihan(

    message:types.Message,

    state:FSMContext

):


    nomor = message.text.strip()



    await message.answer(

        """
🔎 Mengecek tagihan PLN...
"""

    )



    ref_id = (

        "PLN-"

        +

        uuid.uuid4().hex[:8].upper()

    )



    response = digiflazz.inquiry_pasca(

        customer_no=nomor,

        buyer_sku_code="PLN",

        ref_id=ref_id

    )



    print("====================")

    print("[PLN INQUIRY RESPONSE]")

    print(response)

    print("====================")




    if not response:


        await message.answer(

            """
❌ Tagihan tidak ditemukan.

Nomor pelanggan tidak tersedia pada DigiFlazz.
"""

        )


        await state.clear()

        return




    data=response.get(

        "data",

        {}

    )



    nama=data.get(

        "customer_name",

        "-"

    )



    jumlah=data.get(

        "selling_price",

        0

    )



    await message.answer(

        f"""
🧾 TAGIHAN PLN

Nama:
{nama}

Nomor:
{nomor}

Jumlah:
Rp {jumlah:,}


ID:
{ref_id}
"""

    )



    await state.clear()








# =====================================================
# BUAT QRIS TOKEN
# =====================================================

async def buat_qris(

    message,

    order

):


    ref_id=order["ref_id"]

    price=order["price"]



    qris=xendit.create_qris(

        ref_id,

        price

    )



    if not qris:


        await message.answer(

            "❌ Gagal membuat QRIS"

        )

        return



    qr_id=qris.get(

        "id"

    )



    order_repository.update_qr_id(

        ref_id,

        qr_id

    )



    qr_string=qris.get(

        "qr_string"

    )



    qr_url=(

        "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data="

        +

        qr_string

    )



    await message.answer_photo(

        qr_url,


        caption=f"""

🔋 TOKEN PLN

Produk:
{order['product_name']}


Nomor Meter:
{order['customer_no']}


Harga:
Rp {price:,}


ID:
{ref_id}


Silakan bayar QRIS.

"""

    )