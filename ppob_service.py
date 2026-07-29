import requests
import hashlib
import config

def get_digiflazz_price_list():
    """Mengambil daftar harga produk Prabayar (Pulsa, Data, PLN Token, Game)."""
    sign = hashlib.md5(f"{config.DIGIFLAZZ_USERNAME}{config.DIGIFLAZZ_API_KEY}pricelist".encode()).hexdigest()
    payload = {
        "cmd": "prepaid",
        "username": config.DIGIFLAZZ_USERNAME,
        "sign": sign
    }
    try:
        res = requests.post("https://api.digiflazz.com/v1/price-list", json=payload, timeout=15)
        data = res.json()
        
        # Memastikan data yang diterima adalah list produk
        if isinstance(data, dict) and isinstance(data.get("data"), list):
            return data["data"]
            
        # Jika respon berisi pesan error dari DigiFlazz
        if isinstance(data, dict) and isinstance(data.get("data"), dict):
            msg = data["data"].get("message", "Error tidak diketahui")
            print(f"[DIGIFLAZZ PREPAID ERROR] {msg}")
            
        return []
    except Exception as e:
        print(f"[ERROR] get_digiflazz_price_list: {e}")
        return []

def get_digiflazz_pasca_price_list():
    """Mengambil daftar harga produk Pascabayar (PBB, PLN Pasca, BPJS, PDAM, dll)."""
    sign = hashlib.md5(f"{config.DIGIFLAZZ_USERNAME}{config.DIGIFLAZZ_API_KEY}pricelist".encode()).hexdigest()
    payload = {
        "cmd": "pasca",
        "username": config.DIGIFLAZZ_USERNAME,
        "sign": sign
    }
    try:
        res = requests.post("https://api.digiflazz.com/v1/price-list", json=payload, timeout=15)
        data = res.json()
        
        # Memastikan data yang diterima adalah list produk
        if isinstance(data, dict) and isinstance(data.get("data"), list):
            return data["data"]
            
        # Jika respon berisi pesan error dari DigiFlazz
        if isinstance(data, dict) and isinstance(data.get("data"), dict):
            msg = data["data"].get("message", "Error tidak diketahui")
            print(f"[DIGIFLAZZ PASCA ERROR] {msg}")
            
        return []
    except Exception as e:
        print(f"[ERROR] get_digiflazz_pasca_price_list: {e}")
        return []

def send_digiflazz_transaction(customer_no, buyer_sku_code, ref_id):
    """Proses Pembelian Produk Prabayar."""
    sign = hashlib.md5(f"{config.DIGIFLAZZ_USERNAME}{config.DIGIFLAZZ_API_KEY}{ref_id}".encode()).hexdigest()
    payload = {
        "username": config.DIGIFLAZZ_USERNAME,
        "buyer_sku_code": buyer_sku_code,
        "customer_no": str(customer_no),
        "ref_id": ref_id,
        "sign": sign
    }
    try:
        res = requests.post("https://api.digiflazz.com/v1/transaction", json=payload, timeout=15)
        return res.json()
    except Exception as e:
        print(f"[ERROR] send_digiflazz_transaction: {e}")
        return None

def send_digiflazz_inquiry(customer_no, buyer_sku_code, ref_id):
    """Cek Tagihan Pascabayar (Inquire-Pasca)."""
    sign = hashlib.md5(f"{config.DIGIFLAZZ_USERNAME}{config.DIGIFLAZZ_API_KEY}{ref_id}".encode()).hexdigest()
    payload = {
        "commands": "inquire-pasca",
        "username": config.DIGIFLAZZ_USERNAME,
        "buyer_sku_code": buyer_sku_code,
        "customer_no": str(customer_no),
        "ref_id": ref_id,
        "sign": sign
    }
    try:
        res = requests.post("https://api.digiflazz.com/v1/transaction", json=payload, timeout=15)
        return res.json()
    except Exception as e:
        print(f"[ERROR] send_digiflazz_inquiry: {e}")
        return None

def send_digiflazz_pasca_pay(customer_no, buyer_sku_code, ref_id):
    """Bayar Tagihan Pascabayar (Pay-Pasca). Ref_id harus sama persis dengan saat Inquiry."""
    sign = hashlib.md5(f"{config.DIGIFLAZZ_USERNAME}{config.DIGIFLAZZ_API_KEY}{ref_id}".encode()).hexdigest()
    payload = {
        "commands": "pay-pasca",
        "username": config.DIGIFLAZZ_USERNAME,
        "buyer_sku_code": buyer_sku_code,
        "customer_no": str(customer_no),
        "ref_id": ref_id,
        "sign": sign
    }
    try:
        res = requests.post("https://api.digiflazz.com/v1/transaction", json=payload, timeout=15)
        return res.json()
    except Exception as e:
        print(f"[ERROR] send_digiflazz_pasca_pay: {e}")
        return None