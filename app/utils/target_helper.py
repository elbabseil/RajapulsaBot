def get_target_text(product: dict):


    category = str(
        product.get(
            "category",
            ""
        )
    ).upper()


    brand = str(
        product.get(
            "brand",
            ""
        )
    ).upper()


    product_name = str(
        product.get(
            "product_name",
            ""
        )
    ).upper()



    # ==========================
    # PULSA
    # ==========================

    if category == "PULSA":

        return (
            "📱 Silakan kirim nomor HP."
        )



    # ==========================
    # DATA INTERNET
    # ==========================

    if category == "DATA":

        return (
            "📱 Silakan kirim nomor HP."
        )



    # ==========================
    # MASA AKTIF
    # ==========================

    if category == "MASA AKTIF":

        return (
            "📱 Silakan kirim nomor HP."
        )



    # ==========================
    # TOKEN PLN PRABAYAR
    # ==========================

    if category == "PLN":

        return (
            "⚡ Silakan kirim nomor meter "
            "atau ID pelanggan PLN."
        )



    # ==========================
    # GAME TOPUP
    # Contoh:
    # Mobile Legends Diamond
    # Free Fire Diamond
    # PUBG UC
    # ==========================

    if category == "GAMES":

        return (
            "🎮 Silakan kirim User ID Game."
        )



    # ==========================
    # PLN PASCABAYAR
    # ==========================

    if "PLN PASCABAYAR" in brand:

        return (
            "⚡ Silakan kirim ID pelanggan PLN."
        )



    # ==========================
    # PDAM
    # ==========================

    if "PDAM" in brand:

        return (
            "💧 Silakan kirim nomor pelanggan PDAM."
        )



    # ==========================
    # BPJS
    # ==========================

    if "BPJS" in brand:

        return (
            "🏥 Silakan kirim nomor Virtual Account BPJS."
        )



    # ==========================
    # INTERNET PASCABAYAR
    # ==========================

    if "INTERNET" in brand:

        return (
            "🌐 Silakan kirim ID pelanggan Internet."
        )



    # ==========================
    # TV PASCABAYAR
    # ==========================

    if "TV" in brand:

        return (
            "📺 Silakan kirim nomor pelanggan TV."
        )



    # ==========================
    # GAS
    # ==========================

    if "GAS" in brand:

        return (
            "🔥 Silakan kirim nomor pelanggan Gas."
        )



    # ==========================
    # MULTIFINANCE
    # ==========================

    if "MULTIFINANCE" in brand:

        return (
            "💳 Silakan kirim nomor kontrak."
        )



    # ==========================
    # PBB
    # ==========================

    if "PBB" in brand:

        return (
            "🏠 Silakan kirim NOP PBB."
        )



    # ==========================
    # VOUCHER DIGITAL
    #
    # Contoh:
    # Wave Game Coin
    # Voucher Game
    # Voucher Code
    # ==========================

    if category in [
        "VOUCHER",
        "AKTIVASI VOUCHER"
    ]:

        return None



    # ==========================
    # DETEKSI TAMBAHAN
    # BERDASARKAN NAMA PRODUK
    # ==========================

    if any(word in product_name for word in [

        "COIN",
        "VOUCHER",
        "TOKEN",
        "CODE",
        "KODE"

    ]):

        return None



    # ==========================
    # DEFAULT
    # ==========================

    return None