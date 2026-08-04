from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import uuid


from app.services.order_service import order_service
from app.services.digiflazz_service import digiflazz


from app.database.transaction_repository import (
    transaction_repository
)


from app.keyboards.payment_keyboard import (
    bayar_keyboard
)



router = Router()



class PLNState(StatesGroup):

    waiting_meter = State()

    waiting_customer_number = State()




# ==========================================
# MENU PLN
# ==========================================

@router.message(
    F.text == "⚡ PLN"
)
async def pln_menu(message: types.Message):


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
        "⚡ Layanan PLN",
        reply_markup=builder.as_markup()
    )




# ==========================================
# TOKEN PLN MENU
# ==========================================

@router.callback_query(
    F.data=="pln_token"
)
async def token_menu(
    callback:types.CallbackQuery
):


    builder=InlineKeyboardBuilder()


    for text,sku in [

        ("Rp 20.000","pln20"),
        ("Rp 50.000","pln50"),
        ("Rp 100.000","pln100"),
        ("Rp 1.000.000","pln1000")

    ]:


        builder.button(
            text=text,
            callback_data=f"token:{sku}"
        )


    builder.adjust(2)


    await callback.message.answer(
        "🔋 Pilih Token PLN",
        reply_markup=builder.as_markup()
    )


    await callback.answer()




# ==========================================
# PILIH TOKEN
# ==========================================

@router.callback_query(
    F.data.startswith("token:")
)
async def pilih_token(
    callback:types.CallbackQuery,
    state:FSMContext
):


    sku=callback.data.replace(
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
🔋 TOKEN PLN

Masukkan nomor meter PLN:
"""
    )


    await callback.answer()




# ==========================================
# PROSES TOKEN
# ==========================================

@router.message(
    PLNState.waiting_meter
)
async def proses_token(
    message:types.Message,
    state:FSMContext
):


    data=await state.get_data()


    sku=data.get(
        "sku"
    )


    meter=message.text.strip()



    order=order_service.create_order(

        customer_no=meter,

        buyer_sku_code=sku,

        telegram_id=message.from_user.id

    )



    if order.get("status")=="FAILED":


        await message.answer(
            "❌ Produk PLN tidak ditemukan"
        )

        await state.clear()

        return



    ref_id=order["ref_id"]


    transaction_repository.create(

        ref_id,

        message.chat.id,

        sku,

        "Token PLN",

        meter,

        order.get(
            "price",
            0
        )

    )



    await message.answer(

f"""
✅ TRANSAKSI TOKEN PLN


📱 Meter:
{meter}


🆔 ID:
{ref_id}


Silakan tekan BAYAR SEKARANG.
""",

reply_markup=bayar_keyboard(
    ref_id
)

    )


    await state.clear()




# ==========================================
# TAGIHAN PLN
# ==========================================

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
🧾 TAGIHAN PLN

Masukkan nomor pelanggan PLN:
"""
    )


    await callback.answer()




# ==========================================
# INQUIRY PLN
# ==========================================

@router.message(
    PLNState.waiting_customer_number
)
async def proses_tagihan(
    message:types.Message,
    state:FSMContext
):


    nomor=message.text.strip()


    await message.answer(
        "🔎 Mengecek tagihan PLN..."
    )


    ref_id="PLN-"+uuid.uuid4().hex[:8].upper()



    hasil=digiflazz.inquiry_pasca(

        nomor,

        "PLN",

        ref_id

    )



    if not hasil:


        await message.answer(
            "❌ Data PLN tidak ditemukan"
        )

        await state.clear()

        return



    data=hasil.get(
        "data",
        {}
    )



    nama=data.get(
        "customer_name",
        "-"
    )


    total=int(
        data.get(
            "selling_price",
            0
        )
    )



    transaction_repository.create(

        ref_id,

        message.chat.id,

        "PLN",

        "PLN Pascabayar",

        nomor,

        total

    )



    await message.answer(

f"""
🧾 TAGIHAN PLN


Nama:
{nama}


Nomor:
{nomor}


Total:
Rp {total:,}


ID:
{ref_id}


Silakan tekan BAYAR SEKARANG.
""",

reply_markup=bayar_keyboard(
    ref_id
)

    )


    await state.clear()