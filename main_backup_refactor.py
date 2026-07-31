import asyncio
import logging
import time
import uuid


from aiogram import (
    Bot,
    Dispatcher,
    F,
    types
)


from app.workers.payment_worker import payment_worker
from app.workers.payment_worker import payment_worker

from aiogram.filters import Command


from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import (
    State,
    StatesGroup
)

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    ReplyKeyboardBuilder
)


import config


from app.database.transaction_repository import (
    transaction_repository
)


from app.services.digiflazz_service import (
    digiflazz
)


from app.services.xendit_service import (
    xendit
)


from app.workers.payment_worker import (
    payment_worker
)



# ==================================================
# TELEGRAM CONFIG
# ==================================================

bot = Bot(
    token=config.TELEGRAM_BOT_TOKEN
)


dp = Dispatcher()



# ==================================================
# DATABASE INIT
# ==================================================

transaction_repository.create_table()



# ==================================================
# START PAYMENT WORKER
# ==================================================

payment_worker.start()



print(
    "[SYSTEM] Database siap"
)


print(
    "[SYSTEM] Payment Worker aktif"
)




# ==================================================
# GEMINI AI CUSTOMER SERVICE
# ==================================================

try:

    import google.generativeai as genai


    genai.configure(
        api_key=config.GEMINI_API_KEY
    )


    SYSTEM_PROMPT = """

    Kamu adalah Customer Service RajaPulsa Bot.

    Layanan:
    - Pulsa
    - Paket Data
    - Token PLN
    - Voucher Game
    - Tagihan Pascabayar

    Pembayaran menggunakan QRIS otomatis.

    Jika pelanggan bertanya masalah pembayaran,
    arahkan cek riwayat transaksi.

    Jangan pernah memberikan:
    - API KEY
    - Password
    - Data database
    - Sistem internal

    Jawab singkat dan ramah.

    """


    ai_model = genai.GenerativeModel(

        model_name="gemini-1.5-flash",

        system_instruction=SYSTEM_PROMPT

    )


    print(
        "[AI] Gemini aktif"
    )


except Exception as e:


    ai_model = None


    print(
        "[AI ERROR]",
        e
    )





# ==================================================
# FSM STATE
# ==================================================

class Form(StatesGroup):


    waiting_target = State()


    waiting_search = State()





# ==================================================
# MAIN MENU
# ==================================================

def main_menu():


    keyboard = ReplyKeyboardBuilder()



    keyboard.row(

        types.KeyboardButton(
            text="📱 Pulsa"
        ),

        types.KeyboardButton(
            text="📶 Paket Data"
        )

    )


    keyboard.row(

        types.KeyboardButton(
            text="⚡ Token PLN"
        ),

        types.KeyboardButton(
            text="🎮 Voucher"
        )

    )


    keyboard.row(

        types.KeyboardButton(
            text="📋 Tagihan"
        )

    )


    keyboard.row(

        types.KeyboardButton(
            text="📜 Riwayat"
        ),

        types.KeyboardButton(
            text="❓ Bantuan"
        )

    )



    return keyboard.as_markup(
        resize_keyboard=True
    )





# ==================================================
# CACHE PRODUK
# ==================================================

product_cache = {


    "data": [],


    "time": 0


}





def get_products():


    global product_cache



    now = time.time()



    if (

        product_cache["data"]

        and

        now - product_cache["time"]

        < 300

    ):


        return product_cache["data"]




    try:


        data = digiflazz.prepaid_price_list()



        if data:


            product_cache["data"] = data


            product_cache["time"] = now



        return data



    except Exception as e:


        print(
            "[PRODUCT ERROR]",
            e
        )


        return []





# ==================================================
# CACHE PASCABAYAR
# ==================================================

pasca_cache = {


    "data": [],


    "time": 0


}





def get_pasca_products():


    global pasca_cache



    now = time.time()



    if (

        pasca_cache["data"]

        and

        now - pasca_cache["time"]

        < 300

    ):


        return pasca_cache["data"]




    try:


        data = digiflazz.pasca_price_list()



        if data:


            pasca_cache["data"] = data


            pasca_cache["time"] = now



        return data



    except Exception as e:


        print(
            "[PASCA ERROR]",
            e
        )


        return []
# ==================================================
# START COMMAND
# ==================================================

@dp.message(
    Command(
        commands=[
            "start",
            "menu"
        ]
    )
)
async def start_menu(
    message: types.Message,
    state: FSMContext
):

    await state.clear()


    await message.answer(

        """
⚡ *Selamat Datang di RajaPulsa*

🤖 Layanan Digital Otomatis

Tersedia:

📱 Pulsa
📶 Paket Data
⚡ Token PLN
🎮 Voucher Game
📋 Tagihan Pascabayar


💳 Pembayaran menggunakan QRIS otomatis.

Silahkan pilih menu.
        """,

        parse_mode="Markdown",

        reply_markup=main_menu()

    )





# ==================================================
# MENU PULSA
# ==================================================

@dp.message(
    F.text=="📱 Pulsa"
)
async def menu_pulsa(
    message: types.Message
):


    products = get_products()


    brands=set()



    for p in products:


        name=str(
            p.get(
                "product_name",
                ""
            )
        ).lower()



        brand=p.get(
            "brand"
        )


        if (

            brand

            and

            "pulsa" in name

        ):

            brands.add(
                brand
            )




    keyboard=InlineKeyboardBuilder()



    for b in sorted(brands):


        keyboard.button(

            text=b,

            callback_data=f"pulsa_{b}"

        )



    keyboard.adjust(2)



    await message.answer(

        "📱 Pilih Operator Pulsa:",

        reply_markup=keyboard.as_markup()

    )






@dp.callback_query(
    F.data.startswith("pulsa_")
)
async def pulsa_product(
    callback:types.CallbackQuery
):


    brand=callback.data.split("_")[1]


    products=get_products()



    keyboard=InlineKeyboardBuilder()



    for p in products:


        if p.get("brand")==brand:


            name=p.get(
                "product_name"
            )


            price=p.get(
                "price",
                0
            )


            sku=p.get(
                "buyer_sku_code"
            )



            keyboard.button(

                text=f"{name} Rp {price:,}",

                callback_data=f"buy_{sku}_{price}"

            )



    keyboard.adjust(1)



    await callback.message.edit_text(

        f"📱 Pulsa {brand}",

        reply_markup=keyboard.as_markup()

    )



    await callback.answer()







# ==================================================
# MENU PAKET DATA
# ==================================================

@dp.message(
    F.text=="📶 Paket Data"
)
async def menu_data(
    message:types.Message
):


    products=get_products()



    keyboard=InlineKeyboardBuilder()



    brands=set()



    for p in products:


        name=str(
            p.get(
                "product_name",
                ""
            )
        ).lower()



        if (

            "data" in name

            or

            "internet" in name

        ):


            brands.add(
                p.get("brand")
            )



    for b in sorted(brands):


        keyboard.button(

            text=b,

            callback_data=f"data_{b}"

        )



    keyboard.adjust(2)



    await message.answer(

        "📶 Pilih Operator Data:",

        reply_markup=keyboard.as_markup()

    )






@dp.callback_query(
    F.data.startswith("data_")
)
async def data_product(
    callback:types.CallbackQuery
):


    brand=callback.data.split("_")[1]


    products=get_products()


    keyboard=InlineKeyboardBuilder()



    for p in products:


        if p.get("brand")==brand:


            name=p.get(
                "product_name"
            )


            if (

                "data" in name.lower()

                or

                "internet" in name.lower()

            ):


                keyboard.button(

                    text=f"{name} Rp {p.get('price'):,}",

                    callback_data=f"buy_{p.get('buyer_sku_code')}_{p.get('price')}"

                )



    keyboard.adjust(1)



    await callback.message.edit_text(

        f"📶 Paket {brand}",

        reply_markup=keyboard.as_markup()

    )



    await callback.answer()






# ==================================================
# TOKEN PLN
# ==================================================

@dp.message(
    F.text=="⚡ Token PLN"
)

async def menu_pln(
    message:types.Message
):


    products=get_products()



    keyboard=InlineKeyboardBuilder()



    for p in products:


        name=str(
            p.get(
                "product_name",
                ""
            )
        ).lower()



        if "pln" in name:


            keyboard.button(

                text=f"{p.get('product_name')} Rp {p.get('price'):,}",

                callback_data=f"buy_{p.get('buyer_sku_code')}_{p.get('price')}"

            )



    keyboard.adjust(1)



    await message.answer(

        "⚡ Pilih Token PLN:",

        reply_markup=keyboard.as_markup()

    )






# ==================================================
# VOUCHER GAME
# ==================================================

@dp.message(
    F.text=="🎮 Voucher"
)

async def menu_game(
    message:types.Message
):


    products=get_products()



    keyboard=InlineKeyboardBuilder()



    keywords=[

        "game",

        "diamond",

        "voucher",

        "mobile",

        "free",

        "pubg"

    ]



    for p in products:


        name=str(
            p.get(
                "product_name",
                ""
            )
        ).lower()



        if any(
            x in name
            for x in keywords
        ):


            keyboard.button(

                text=f"{p.get('product_name')} Rp {p.get('price'):,}",

                callback_data=f"buy_{p.get('buyer_sku_code')}_{p.get('price')}"

            )



    keyboard.adjust(1)



    await message.answer(

        "🎮 Pilih Voucher Game:",

        reply_markup=keyboard.as_markup()

    )






# ==================================================
# TAGIHAN PASCABAYAR
# ==================================================

@dp.message(
    F.text=="📋 Tagihan"
)

async def menu_pasca(
    message:types.Message
):


    products=get_pasca_products()


    keyboard=InlineKeyboardBuilder()



    for p in products[:30]:


        keyboard.button(

            text=p.get(
                "product_name",
                "Tagihan"
            ),

            callback_data=f"buy_pasca_{p.get('buyer_sku_code')}"

        )



    keyboard.adjust(1)



    await message.answer(

        "📋 Pilih layanan Pascabayar:",

        reply_markup=keyboard.as_markup()

    )





# ==================================================
# PILIH PRODUK
# ==================================================

@dp.callback_query(
    F.data.startswith("buy_")
)

async def choose_product(
    callback:types.CallbackQuery,
    state:FSMContext
):


    data=callback.data.split("_")



    sku=data[1]


    price=int(
        data[2]
    )



    await state.update_data(

        sku=sku,

        price=price,

        pasca=False

    )



    await state.set_state(
        Form.waiting_target
    )



    await callback.message.answer(

        """
🆔 Masukkan nomor tujuan:

Contoh:

08123456789

atau

ID pelanggan PLN
        """
    )


    await callback.answer()
# ==================================================
# START BOT
# ==================================================

async def main():

    print("[BOT] Telegram polling aktif")

    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())

# ==================================================
# RUN BOT
# ==================================================

async def main():

    print("[BOT] RajaPulsa Bot berjalan...")

    await dp.start_polling(
        bot
    )


if __name__ == "__main__":

    asyncio.run(main())