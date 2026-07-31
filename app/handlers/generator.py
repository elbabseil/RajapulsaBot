from datetime import datetime


def generate_receipt(transaction):

    category = transaction.get("category", "default")

    if category == "pulsa":
        return generate_pulsa(transaction)

    elif category == "game":
        return generate_game(transaction)

    elif category == "pln":
        return generate_pln(transaction)

    elif category == "bpjs":
        return generate_bpjs(transaction)

    else:
        return generate_default(transaction)



def generate_pulsa(data):

    return f"""
===== RAJA PULSA DIGITAL =====

Tanggal : {datetime.now()}

LAYANAN PULSA

Produk  : {data.get('product')}
Nomor   : {data.get('customer')}

Harga   : Rp{data.get('price')}

Status  : {data.get('status')}
SN      : {data.get('sn')}

==============================
"""


def generate_game(data):

    return f"""
===== RAJA PULSA DIGITAL =====

TOP UP GAME

Game     : {data.get('game')}
User ID  : {data.get('user_id')}
Zone ID  : {data.get('zone_id')}

Produk   : {data.get('product')}
Harga    : Rp{data.get('price')}

Status   : {data.get('status')}

==============================
"""


def generate_pln(data):

    return f"""
===== RAJA PULSA DIGITAL =====

TAGIHAN PLN

ID Pelanggan : {data.get('customer_id')}
Nama         : {data.get('name')}
Nominal      : Rp{data.get('price')}

Token/SN     : {data.get('token')}

Status       : {data.get('status')}

==============================
"""


def generate_bpjs(data):

    return f"""
===== RAJA PULSA DIGITAL =====

PEMBAYARAN BPJS

VA Number : {data.get('va')}
Nama      : {data.get('name')}
Periode   : {data.get('period')}

Tagihan   : Rp{data.get('price')}
Admin     : Rp{data.get('admin')}

Status    : {data.get('status')}

==============================
"""


def generate_default(data):

    return f"""
===== RAJA PULSA DIGITAL =====

Layanan : {data.get('product')}
Harga   : Rp{data.get('price')}
Status  : {data.get('status')}

==============================
"""