import hashlib
import json
import requests

# =====================================================
# KONFIGURASI
# =====================================================

USERNAME = "vilopag4aB6o"

# Gunakan Development Key sesuai contoh resmi DigiFlazz
API_KEY = "dev-6deac100-8965-11f1-8255-9fad25ae0611"

BUYER_SKU_CODE = "test"
CUSTOMER_NO = "087800001233"
REF_ID = "TEST001"

URL = "https://api.digiflazz.com/v1/transaction"

# =====================================================
# MEMBUAT SIGNATURE
# =====================================================

raw_sign = USERNAME + API_KEY + REF_ID

sign = hashlib.md5(
    raw_sign.encode("utf-8")
).hexdigest()

payload = {
    "username": USERNAME,
    "buyer_sku_code": BUYER_SKU_CODE,
    "customer_no": CUSTOMER_NO,
    "ref_id": REF_ID,
    "sign": sign
}

# =====================================================
# DEBUG
# =====================================================

print("=" * 60)
print("DIGIFLAZZ TEST")
print("=" * 60)

print("USERNAME :", USERNAME)
print("API KEY  :", API_KEY)
print("REF ID   :", REF_ID)
print()

print("RAW SIGN :")
print(raw_sign)
print()

print("MD5 SIGN :")
print(sign)
print()

print("PAYLOAD :")
print(json.dumps(payload, indent=4))
print()

# =====================================================
# REQUEST
# =====================================================

try:

    response = requests.post(
        URL,
        json=payload,
        timeout=30
    )

    print("=" * 60)
    print("HTTP STATUS")
    print("=" * 60)
    print(response.status_code)
    print()

    print("=" * 60)
    print("RESPONSE")
    print("=" * 60)

    try:
        print(json.dumps(response.json(), indent=4))
    except Exception:
        print(response.text)

except Exception as e:

    print()
    print("ERROR")
    print(e)