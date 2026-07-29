import asyncio
import logging
import uuid
import time
import google.generativeai as genai
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import config
import database
import ppob_service
import payment_service

bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

database.init_db()

# --- INISIALISASI GEMINI AI CS ---
try:
    genai.configure(api_key=config.GEMINI_API_KEY)
    SYSTEM_PROMPT = """
    Kamu adalah Customer Service otomatis yang ramah, sopan, dan solutif untuk 'RajaPulsa Bot'.

    Informasi Bot:
    - Layanan: Menjual Pulsa Regular, Paket Data, Token PLN, Voucher Game, dan Tagihan Pascabayar, PDAM, PLN, PBB.
    - Pembayaran: Menggunakan QRIS Instant. Pembayaran diverifikasi secara otomatis.
    - Kendala Pembayaran: Jika pengguna sudah bayar tapi produk belum masuk, arahkan untuk tekan menu '📜 Riwayat Transaksi' atau tombol '🔄 Cek Pembayaran & Proses' pada pesan QRIS.

    Aturan Jawaban:
    - Jawab pertanyaan pengguna secara singkat, jelas, padat, dan ramah.
    - Gunakan bahasa Indonesia sehari-hari yang santai namun sopan.
    - DILARANG memberitahukan API Key, password, atau struktur sistem internal bot.
    """
    ai_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
    print("[AI] Google Gemini AI berhasil diinisialisasi.")
except Exception as e:
    ai_model = None
    print(f"[WARNING] Gagal mengkonfigurasi Gemini AI: {e}")

class Form(StatesGroup):
    waiting_for_custom_target = State()
    waiting_for_search_query = State()

def get_main_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="📱 Pulsa Regular"),
        types.KeyboardButton(text="📶 Paket Data")
    )
    builder.row(
        types.KeyboardButton(text="⚡ Token PLN"),
        types.KeyboardButton(text="🎮 Voucher Game")
    )
    builder.row(
        types.KeyboardButton(text="📋 Tagihan (Dll)")
    )
    builder.row(
        types.KeyboardButton(text="📜 Riwayat Transaksi"),
        types.KeyboardButton(text="📋 Cek Status / Bantuan")
    )
    return builder.as_markup(resize_keyboard=True)

# --- CACHE PRODUK PRABAYAR ---
_product_cache = {
    "data": [],
    "last_fetched": 0
}

def fetch_products():
    global _product_cache
    current_time = time.time()
    
    if _product_cache["data"] and (current_time - _product_cache["last_fetched"] < 300):
        products = _product_cache["data"]
    else:
        products = ppob_service.get_digiflazz_price_list()
        if isinstance(products, dict):
            products = list(products.values())
        elif not isinstance(products, list):
            products = []

        if products:
            _product_cache["data"] = products
            _product_cache["last_fetched"] = current_time
            print(f"[CACHE] Berhasil memperbarui {len(products)} produk Prabayar dari DigiFlazz.")
        elif _product_cache["data"]:
            print("[WARNING] Server DigiFlazz mengembalikan data kosong. Menggunakan cache prabayar sebelumnya.")
            products = _product_cache["data"]
            
    if isinstance(products, dict):
        return list(products.values())
    elif not isinstance(products, list):
        return []
    return products

# --- CACHE PRODUK PASCABAYAR ---
_pasca_product_cache = {
    "data": [],
    "last_fetched": 0
}

def fetch_pasca_products():
    global _pasca_product_cache
    current_time = time.time()
    
    if _pasca_product_cache["data"] and (current_time - _pasca_product_cache["last_fetched"] < 300):
        products = _pasca_product_cache["data"]
    else:
        products = ppob_service.get_digiflazz_pasca_price_list()
        if isinstance(products, dict):
            products = list(products.values())
        elif not isinstance(products, list):
            products = []

        if products:
            _pasca_product_cache["data"] = products
            _pasca_product_cache["last_fetched"] = current_time
            print(f"[CACHE] Berhasil memperbarui {len(products)} produk Pascabayar dari DigiFlazz.")
        elif _pasca_product_cache["data"]:
            print("[WARNING] Server DigiFlazz mengembalikan data kosong. Menggunakan cache pascabayar sebelumnya.")
            products = _pasca_product_cache["data"]

    if isinstance(products, dict):
        return list(products.values())
    elif not isinstance(products, list):
        return []
    return products

@dp.message(Command(commands=['start', 'menu', 'cancel']))
async def handle_start(message: types.Message, state: FSMContext):
    await state.clear()
    welcome_text = (
        "⚡ *Selamat datang di RajaPulsa Bot!*\n\n"
        "🤖 *Pusat Pembelian Pulsa, Token PLN, Game, & Tagihan Otomatis*\n"
        "💳 *Sistem Bayar Langsung (QRIS Instant per Transaksi)*\n\n"
        "👇 Silakan pilih menu di bawah:"
    )
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=get_main_menu_keyboard())

# --- DAFTAR OPERATOR TELEKOMUNIKASI UTAMA ---
OPERATOR_BRANDS = ["TELKOMSEL", "INDOSAT", "XL", "AXIS", "TRI", "SMARTFREN", "BY.U"]

# --- KATEGORI: PULSA REGULAR ---
@dp.message(F.text == "📱 Pulsa Regular")
async def category_pulsa(message: types.Message):
    products = fetch_products()
    
    valid_brands = set()
    for p in products:
        if not isinstance(p, dict):
            continue
        brand = str(p.get("brand", "")).strip().upper()
        name = str(p.get("product_name", "")).lower()
        if brand in OPERATOR_BRANDS and "pulsa" in name and "data" not in name and "paket" not in name:
            valid_brands.add(p.get("brand"))
            
    if not valid_brands:
        valid_brands = set(OPERATOR_BRANDS)

    brands = sorted(list(valid_brands))
    if not brands:
        await message.answer("❌ Produk Pulsa sedang kosong / gangguan.", reply_markup=get_main_menu_keyboard())
        return

    builder = InlineKeyboardBuilder()
    for b in brands:
        builder.button(text=b, callback_data=f"pulsabrand_{b}")
    builder.adjust(2)

    await message.answer("📱 *Pilih Operator Pulsa Regular:*", parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("pulsabrand_"))
async def show_pulsa_products(callback: types.CallbackQuery):
    brand_name = callback.data.split("_", 1)[1].strip()
    products = fetch_products()
    
    filtered = [p for p in products if isinstance(p, dict) and str(p.get("brand", "")).strip().upper() == brand_name.upper() and "pulsa" in str(p.get("product_name", "")).lower() and "data" not in str(p.get("product_name", "")).lower()]

    if not filtered:
        filtered = [p for p in products if isinstance(p, dict) and str(p.get("brand", "")).strip().upper() == brand_name.upper()]

    builder = InlineKeyboardBuilder()
    for p in filtered[:15]:
        name = p.get("product_name")
        price = p.get("price", 0) + 0  # Margin diubah menjadi 0
        sku = p.get("buyer_sku_code")
        builder.button(text=f"{name} (Rp {price:,})", callback_data=f"buyprod_{sku}_{price}")
    builder.adjust(1)

    await callback.message.edit_text(f"📱 *Pilih Nominal Pulsa {brand_name}:*", parse_mode="Markdown", reply_markup=builder.as_markup())
    await callback.answer()

# --- KATEGORI: PAKET DATA ---
@dp.message(F.text == "📶 Paket Data")
async def category_data(message: types.Message):
    products = fetch_products()
    
    data_brands = set()
    for p in products:
        if not isinstance(p, dict):
            continue
        brand = str(p.get("brand", "")).strip().upper()
        name = str(p.get("product_name", "")).lower()
        cat = str(p.get("category", "")).lower()
        if brand in OPERATOR_BRANDS and ("data" in name or "paket" in name or "internet" in name or "data" in cat or "aon" in name):
            data_brands.add(p.get("brand"))

    if not data_brands:
        data_brands = set(OPERATOR_BRANDS)

    brands = sorted(list(data_brands))
    if not brands:
        await message.answer("❌ Produk Paket Data sedang kosong / gangguan.", reply_markup=get_main_menu_keyboard())
        return

    builder = InlineKeyboardBuilder()
    for b in brands:
        builder.button(text=b, callback_data=f"databrand_{b}")
    builder.adjust(2)

    await message.answer("📶 *Pilih Operator Paket Data:*", parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("databrand_"))
async def show_data_products(callback: types.CallbackQuery):
    brand_name = callback.data.split("_", 1)[1].strip()
    products = fetch_products()
    
    filtered = [p for p in products if isinstance(p, dict) and str(p.get("brand", "")).strip().upper() == brand_name.upper() and ("data" in str(p.get("product_name", "")).lower() or "paket" in str(p.get("product_name", "")).lower() or "internet" in str(p.get("product_name", "")).lower())]

    if not filtered:
        filtered = [p for p in products if isinstance(p, dict) and str(p.get("brand", "")).strip().upper() == brand_name.upper()]

    builder = InlineKeyboardBuilder()
    for p in filtered[:15]:
        name = p.get("product_name")
        price = p.get("price", 0) + 0  # Margin diubah menjadi 0
        sku = p.get("buyer_sku_code")
        builder.button(text=f"{name} (Rp {price:,})", callback_data=f"buyprod_{sku}_{price}")
    builder.adjust(1)

    await callback.message.edit_text(f"📶 *Pilih Paket Data {brand_name}:*", parse_mode="Markdown", reply_markup=builder.as_markup())
    await callback.answer()

# --- KATEGORI: TOKEN PLN ---
@dp.message(F.text == "⚡ Token PLN")
async def category_pln(message: types.Message):
    products = fetch_products()
    
    pln_products = [p for p in products if isinstance(p, dict) and (str(p.get("brand", "")).strip().upper() == "PLN" or "pln" in str(p.get("category", "")).lower() or "token" in str(p.get("product_name", "")).lower())]
    
    if not pln_products:
        pln_products = [p for p in products if isinstance(p, dict) and "pln" in str(p.get("product_name", "")).lower()]

    if not pln_products:
        await message.answer("❌ Maaf, produk Token PLN sedang kosong / gangguan.", reply_markup=get_main_menu_keyboard())
        return

    text = "⚡ *Pilih Nominal Token PLN Tersedia:*"
    builder = InlineKeyboardBuilder()
    for p in pln_products[:12]:
        product_name = p.get("product_name")
        price = p.get("price", 0) + 0  # Margin diubah menjadi 0
        sku = p.get("buyer_sku_code")
        builder.button(text=f"{product_name} (Rp {price:,})", callback_data=f"buyprod_{sku}_{price}")
    builder.adjust(2)
    
    await message.answer(text, parse_mode="Markdown", reply_markup=builder.as_markup())

# --- KATEGORI: VOUCHER GAME ---
@dp.message(F.text == "🎮 Voucher Game")
async def category_game(message: types.Message):
    products = fetch_products()
    
    game_keywords = ["free fire", "mobile legends", "pubg", "valorant", "steam", "garena", "call of duty", "hago", "gem", "diamond", "uc", "voucher"]
    game_brands = set()
    for p in products:
        if not isinstance(p, dict):
            continue
        brand = str(p.get("brand", ""))
        cat = str(p.get("category", "")).lower()
        name = str(p.get("product_name", "")).lower()
        if "game" in cat or "voucher" in cat or any(kw in name or kw in brand.lower() for kw in game_keywords):
            if brand.strip().upper() not in OPERATOR_BRANDS and brand.strip().upper() != "PLN":
                game_brands.add(brand.strip())

    brands = sorted(list(game_brands))
    if not brands:
        brands = sorted(list(set(str(p.get("brand")).strip() for p in products if isinstance(p, dict) and p.get("brand") and str(p.get("brand")).strip().upper() not in OPERATOR_BRANDS and str(p.get("brand")).strip().upper() != "PLN")))[:20]

    if not brands:
        await message.answer("❌ Maaf, produk Voucher Game belum tersedia.", reply_markup=get_main_menu_keyboard())
        return

    text = "🎮 *Pilih Game / Brand Tersedia:*"
    builder = InlineKeyboardBuilder()
    for b in brands[:20]:
        builder.button(text=b, callback_data=f"gamebrand_{b}")
    builder.adjust(2)
    
    await message.answer(text, parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("gamebrand_"))
async def show_game_products(callback: types.CallbackQuery):
    brand_name = callback.data.split("_", 1)[1].strip()
    products = fetch_products()
    
    filtered = [p for p in products if isinstance(p, dict) and str(p.get("brand", "")).strip().upper() == brand_name.upper()]

    text = f"🎮 *Pilih Item untuk {brand_name}:*"
    builder = InlineKeyboardBuilder()
    for p in filtered[:15]:
        name = p.get("product_name")
        price = p.get("price", 0) + 0  # Margin diubah menjadi 0
        sku = p.get("buyer_sku_code")
        builder.button(text=f"{name} - Rp {price:,}", callback_data=f"buyprod_{sku}_{price}")
    builder.adjust(1)
    
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=builder.as_markup())
    await callback.answer()

# --- KATEGORI: TAGIHAN (PASCABAYAR) ---
@dp.message(F.text == "📋 Tagihan (Dll)")
async def menu_tagihan(message: types.Message, state: FSMContext):
    await state.clear()
    pasca_products = fetch_pasca_products()
    
    valid_tagihan_brands = set()
    for p in pasca_products:
        if isinstance(p, dict) and p.get("brand"):
            valid_tagihan_brands.add(str(p.get("brand")).strip())

    brands = sorted(list(valid_tagihan_brands))

    if not brands:
        await message.answer("❌ Produk Tagihan sedang kosong atau gangguan. Cek IP Whitelist / API Key DigiFlazz kamu.", reply_markup=get_main_menu_keyboard())
        return

    builder = InlineKeyboardBuilder()
    builder.button(text="🔍 Cari Nama Kota / Daerah", callback_data="search_tagihan_trigger")
    for b in brands[:15]:
        builder.button(text=b, callback_data=f"tagihanbrand_{b}")
    builder.adjust(1)

    await message.answer("📋 *Pilih Jenis Layanan / Tagihan atau Cari Berdasarkan Nama:*", parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "search_tagihan_trigger")
async def trigger_search_mode(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.waiting_for_search_query)
    
    builder = ReplyKeyboardBuilder()
    builder.button(text="❌ Batal Cari")
    
    await callback.message.answer(
        "🔍 *Fitur Pencarian Layanan*\n\n"
        "Silakan ketik nama kota atau daerah yang ingin Anda cari (Contoh: *Bandung*, *Jakarta*, *Semarang*):",
        parse_mode="Markdown",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
    await callback.answer()

@dp.message(Form.waiting_for_search_query)
async def process_search_query(message: types.Message, state: FSMContext):
    if message.text == "❌ Batal Cari":
        await state.clear()
        await handle_start(message, state)
        return

    keyword = message.text.strip().lower()
    pasca_products = fetch_pasca_products()
    
    filtered = [
        p for p in pasca_products 
        if isinstance(p, dict) and (
            keyword in str(p.get("product_name", "")).lower() or 
            keyword in str(p.get("brand", "")).lower() or
            keyword in str(p.get("pasca_name", "")).lower()
        )
    ]

    if not filtered:
        await message.answer(
            f"❌ Tidak ditemukan layanan dengan kata kunci *'{message.text}'*.\n"
            "Silakan ketik kata kunci lain atau ketik *'❌ Batal Cari'* untuk kembali.",
            parse_mode="Markdown"
        )
        return

    builder = InlineKeyboardBuilder()
    for p in filtered[:15]:
        name = p.get("pasca_name") or p.get("product_name") or "Layanan"
        sku = p.get("buyer_sku_code")
        builder.button(text=f"{name}", callback_data=f"buyprod_{sku}_PASCA")
    builder.adjust(1)

    await message.answer(
        f"🔍 *Hasil pencarian untuk '{message.text}':* (Ditemukan {len(filtered)} layanan)",
        parse_mode="Markdown",
        reply_markup=builder.as_markup()
    )
    await state.clear()

@dp.callback_query(F.data.startswith("tagihanbrand_"))
async def show_tagihan_products(callback: types.CallbackQuery):
    brand_name = callback.data.split("_", 1)[1].strip()
    pasca_products = fetch_pasca_products()
        
    filtered = [p for p in pasca_products if isinstance(p, dict) and str(p.get("brand", "")).strip().upper() == brand_name.upper()]
    
    if not filtered:
        products = fetch_products()
        filtered = [p for p in products if isinstance(p, dict) and str(p.get("brand", "")).strip().upper() == brand_name.upper()]

    if not filtered:
        await callback.answer("❌ Produk untuk layanan ini sedang tidak tersedia.", show_alert=True)
        return

    builder = InlineKeyboardBuilder()
    builder.button(text="🔍 Cari Nama Kota Lainnya", callback_data="search_tagihan_trigger")
    
    for p in filtered[:15]:
        name = p.get("pasca_name") or p.get("product_name") or f"Tagihan {brand_name}"
        sku = p.get("buyer_sku_code")
        builder.button(text=f"{name}", callback_data=f"buyprod_{sku}_PASCA")
    builder.adjust(1)
    
    await callback.message.edit_text(f"📋 *Pilih Layanan {brand_name}:*", parse_mode="Markdown", reply_markup=builder.as_markup())
    await callback.answer()

# --- PROSES PEMBELIAN & QRIS ---
@dp.callback_query(F.data.startswith("buyprod_"))
async def ask_target_number(callback: types.CallbackQuery, state: FSMContext):
    data_part = callback.data.removeprefix("buyprod_")
    try:
        sku, price_str = data_part.rsplit("_", 1)
        is_pasca = (price_str == "PASCA")
        price = 0 if is_pasca else int(price_str)
    except ValueError:
        await callback.answer("❌ Format data produk tidak valid.", show_alert=True)
        return
    
    pasca_list = fetch_pasca_products()
    products = fetch_products() + pasca_list
    
    product_name = "Produk Digital"
    for p in products:
        if not isinstance(p, dict):
            continue
        if p.get("buyer_sku_code") == sku:
            product_name = p.get("pasca_name") or p.get("product_name") or "Produk Digital"
            break

    await state.update_data(sku=sku, price=price, product_name=product_name, is_pasca=is_pasca)
    await state.set_state(Form.waiting_for_custom_target)

    builder = ReplyKeyboardBuilder()
    builder.button(text="❌ Batal")
    
    await callback.message.answer(
        "🆔 *Masukkan Nomor Tujuan / No Pelanggan / NOP PBB:*\n*(Contoh: 08123456789 atau ID Pelanggan PLN/PDAM/PBB)*", 
        parse_mode="Markdown", 
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
    await callback.answer()

@dp.message(Form.waiting_for_custom_target)
async def process_custom_target(message: types.Message, state: FSMContext):
    if message.text == "❌ Batal":
        await handle_start(message, state)
        return

    data = await state.get_data()
    sku = data.get("sku")
    price = data.get("price", 0)
    product_name = data.get("product_name")
    is_pasca = data.get("is_pasca", False)

    target_no = message.text.strip()
    chat_id = message.chat.id
    ref_id = f"TRX{uuid.uuid4().hex[:10]}"

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # ALUR A: PASCABAYAR (INQUIRY / CEK TAGIHAN DULU)
    if is_pasca or price == 0:
        await message.answer("🔄 *Sedang memeriksa tagihan ke server...*", parse_mode="Markdown")
        inq_res = ppob_service.send_digiflazz_inquiry(target_no, sku, ref_id)
        
        if inq_res and "data" in inq_res:
            inq_data = inq_res["data"]
            status = str(inq_data.get("status", "")).lower()
            
            if status in ["sukses", "success", "pending"]:
                customer_name = inq_data.get("customer_name", "Pelanggan")
                tagihan_amount = inq_data.get("price", 0)
                admin_fee = inq_data.get("admin", 2500)
                margin_bot = 0  # Keuntungan bot diatur 0
                total_pay = tagihan_amount + admin_fee + margin_bot

                price = total_pay
                
                # Ekstraksi Rincian Tambahan
                desc_info = ""
                desc_data = inq_data.get("desc", {})
                if isinstance(desc_data, dict):
                    lembar = desc_data.get("lembar_tagihan") or desc_data.get("jumlah_tagihan")
                    tarif = desc_data.get("tarif") or desc_data.get("daya")
                    kab_kota = desc_data.get("kab_kota") or desc_data.get("kota")
                    tahun = desc_data.get("tahun") or desc_data.get("tahun_pajak")
                    detail_list = desc_data.get("detail", [])
                    
                    if lembar:
                        desc_info += f"\n📄 Lembar Tagihan: {lembar}"
                    if tarif:
                        desc_info += f"\n⚡ Daya / Tarif   : {tarif}"
                    if tahun:
                        desc_info += f"\n📅 Tahun Pajak   : {tahun}"
                    if kab_kota:
                        desc_info += f"\n📍 Wilayah       : {kab_kota}"
                    if isinstance(detail_list, list) and len(detail_list) > 0:
                        first_det = detail_list[0]
                        if isinstance(first_det, dict):
                            periode = first_det.get("periode")
                            if periode:
                                desc_info += f"\n📅 Periode       : {periode}"

                info_text = (
                    f"📄 *RINCIAN TAGIHAN PASCABAYAR*\n"
                    f"-----------------------------------\n"
                    f"📦 Produk        : {product_name}\n"
                    f"👤 Nama Pelanggan: *{customer_name}*\n"
                    f"🎯 No Pelanggan  : `{target_no}`"
                    f"{desc_info}\n"
                    f"💰 Tagihan Pokok : Rp {tagihan_amount:,}\n"
                    f"💵 Admin         : Rp {admin_fee:,}\n"
                    f"-----------------------------------\n"
                    f"💳 *Total Harus Dibayar: Rp {total_pay:,}*"
                )
                await message.answer(info_text, parse_mode="Markdown")
            else:
                msg = inq_data.get("message", "Tagihan tidak ditemukan / sudah terbayar.")
                await message.answer(f"❌ *Cek Tagihan Gagal:* {msg}", reply_markup=get_main_menu_keyboard())
                await state.clear()
                return
        else:
            await message.answer("❌ Gagal mengecek tagihan ke DigiFlazz. Pastikan No Pelanggan benar.", reply_markup=get_main_menu_keyboard())
            await state.clear()
            return

    # ALUR B: BUAT QRIS XENDIT
    await message.answer("🔄 Memproses pembuatan QRIS Xendit...", parse_mode="Markdown")
    qris_res = payment_service.create_xendit_qris(price, ref_id)
    
    if qris_res and ("qr_string" in qris_res or "qr_code" in qris_res):
        qris_string = qris_res.get("qr_string") or qris_res.get("qr_code")
        
        database.save_transaction(
            trx_id=ref_id, 
            user_id=chat_id, 
            product_name=f"{product_name} ({'PASCA' if is_pasca else 'PRA'})", 
            phone_number=target_no, 
            nominal=price, 
            status="PENDING"
        )

        qris_caption = (
            f"⚡ *Tagihan Pembayaran Instant*\n\n"
            f"📦 Produk : {product_name}\n"
            f"🎯 Tujuan : `{target_no}`\n"
            f"💰 Total Bayar: *Rp {price:,}*\n"
            f"🆔 ID TRX : `{ref_id}`\n\n"
            f"⚠️ *Silakan Scan QRIS di atas untuk membayar.* Pesanan akan otomatis diproses setelah pembayaran lunas."
        )

        trx_type = "PASCA" if is_pasca else "PRA"
        builder = InlineKeyboardBuilder()
        builder.button(text="🔄 Cek Pembayaran & Proses", callback_data=f"checkpay_{ref_id}_{sku}_{trx_type}")
        builder.adjust(1)

        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={qris_string}"
        await bot.send_photo(chat_id, photo=qr_url, caption=qris_caption, parse_mode="Markdown", reply_markup=builder.as_markup())
    else:
        await message.answer("❌ Gagal membuat tagihan QRIS Xendit. Silakan coba beberapa saat lagi.", reply_markup=get_main_menu_keyboard())
    
    await state.clear()

@dp.callback_query(F.data.startswith("checkpay_"))
async def process_check_payment(callback: types.CallbackQuery):
    await callback.answer("Memeriksa status pembayaran...")
    data_part = callback.data.removeprefix("checkpay_")
    
    try:
        parts = data_part.split("_")
        ref_id = parts[0]
        sku = parts[1]
        trx_type = parts[2] if len(parts) > 2 else "PRA"
    except Exception:
        ref_id = data_part
        sku = ""
        trx_type = "PRA"

    chat_id = callback.message.chat.id

    status_response = payment_service.check_xendit_status(ref_id)
    if status_response:
        payment_status = str(status_response.get("status", "")).upper()
        if payment_status in ["COMPLETED", "SUCCESS", "PAID", "ACTIVE"]:
            trx_data = database.get_transaction(ref_id)
            if trx_data and trx_data["status"] != "SUCCESS":
                database.update_status(trx_id=ref_id, status="PROCESSING")
                
                await bot.send_message(chat_id, "✅ *Pembayaran Berhasil!* Mengirim pesanan ke server DigiFlazz...", parse_mode="Markdown")
                
                target_no = trx_data["phone_number"]
                price = trx_data["nominal"]

                if trx_type == "PASCA":
                    df_res = ppob_service.send_digiflazz_pasca_pay(target_no, sku, ref_id)
                else:
                    df_res = ppob_service.send_digiflazz_transaction(target_no, sku, ref_id)

                if df_res and "data" in df_res:
                    df_data = df_res["data"]
                    df_status = df_data.get("status", "Pending")
                    df_message = df_data.get("message", "Diproses")
                    
                    if str(df_status).lower() in ["sukses", "success"]:
                        database.update_status(ref_id, "SUCCESS")
                        status_label = "BERHASIL ✅"
                    else:
                        database.update_status(ref_id, "PENDING")
                        status_label = f"PENDING / DIPROSES ({df_message})"

                    receipt = (
                        f"📄 *STRUK TRANSAKSI SUKSES*\n"
                        f"-----------------------------------\n"
                        f"🆔 ID TRX : `{ref_id}`\n"
                        f"📦 Produk : {trx_data['product_name']}\n"
                        f"🎯 Tujuan : {target_no}\n"
                        f"💰 Harga  : Rp {price:,}\n"
                        f"Status    : {status_label}\n"
                        f"-----------------------------------"
                    )
                    await bot.send_message(chat_id, receipt, parse_mode="Markdown", reply_markup=get_main_menu_keyboard())
                    try:
                        await callback.message.delete()
                    except Exception:
                        pass
                else:
                    database.update_status(ref_id, "FAILED")
                    await bot.send_message(chat_id, "❌ Pembayaran diterima, tetapi gagal menghubungi server DigiFlazz. Hubungi admin.", reply_markup=get_main_menu_keyboard())
            else:
                await bot.send_message(chat_id, "⚠️ Transaksi ini sudah pernah diproses sebelumnya.")
        else:
            await bot.send_message(chat_id, f"⏳ Pembayaran belum terdeteksi (Status: {payment_status}). Silakan selesaikan pembayaran QRIS terlebih dahulu.")
    else:
        await callback.message.answer("❌ Gagal memeriksa status pembayaran ke Xendit.")

# --- RIWAYAT TRANSAKSI ---
@dp.message(F.text == "📜 Riwayat Transaksi")
async def menu_history(message: types.Message):
    chat_id = message.chat.id
    history = database.get_user_transactions(chat_id, limit=5)

    if not history:
        await message.answer("📜 Anda belum memiliki riwayat transaksi.", reply_markup=get_main_menu_keyboard())
        return

    await message.answer("📜 *5 Transaksi Terakhir Anda:*", parse_mode="Markdown")
    for t in history:
        status_emoji = "✅" if t["status"] == "SUCCESS" else "⏳"
        receipt_text = (
            f"📄 *STRUK DIGITAL*\n"
            f"-----------------------------------\n"
            f"🆔 ID TRX : `{t['trx_id']}`\n"
            f"📅 Waktu  : {t['created_at']}\n"
            f"📦 Produk : {t['product_name']}\n"
            f"🎯 Tujuan : {t['phone_number']}\n"
            f"💰 Harga  : Rp {t['nominal']:,}\n"
            f"Status    : {status_emoji} {t['status']}\n"
            f"-----------------------------------"
        )
        await message.answer(receipt_text, parse_mode="Markdown")
    await message.answer("Kembali ke Menu Utama:", reply_markup=get_main_menu_keyboard())

# --- BANTUAN ---
@dp.message(F.text == "📋 Cek Status / Bantuan")
async def handle_help_status(message: types.Message):
    help_text = (
        "📋 *Bantuan & Informasi Bot*\n\n"
        "• Bot ini menggunakan sistem *Bayar Langsung (Direct QRIS)*.\n"
        "• Mendukung Pulsa, Paket Data, Token PLN, Game, hingga Tagihan Pascabayar.\n"
        "• Gunakan menu *📜 Riwayat Transaksi* untuk melihat struk pembelian Anda.\n"
        "• Anda juga dapat mengetik pertanyaan secara bebas di sini untuk dijawab oleh CS AI kami!"
    )
    await message.answer(help_text, parse_mode="Markdown", reply_markup=get_main_menu_keyboard())

# --- HANDLER AI CUSTOMER SERVICE (FALLBACK TEXT) ---
@dp.message(F.text)
async def ai_customer_service(message: types.Message):
    if not ai_model:
        await message.answer("Silakan pilih menu transaksi di bawah:", reply_markup=get_main_menu_keyboard())
        return

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    try:
        response = ai_model.generate_content(message.text)
        if response and response.text:
            await message.answer(response.text, parse_mode="Markdown")
        else:
            await message.answer("Maaf, aku tidak dapat memahami pertanyaan tersebut. Silakan pilih menu di bawah:", reply_markup=get_main_menu_keyboard())
    except Exception as e:
        logging.error(f"Error AI: {e}")
        await message.answer("Maaf, layanan CS sedang tidak dapat merespon. Silakan gunakan menu di bawah ya!", reply_markup=get_main_menu_keyboard())

async def main():
    print("==================================================")
    print("⚡ RajaPulsaOfficial_bot (Direct QRIS Xendit + AI CS) Berjalan...")
    print("Tekan CTRL+C untuk menghentikan.")
    print("==================================================")
    await dp.start_polling(bot, skip_pending=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot dihentikan.")