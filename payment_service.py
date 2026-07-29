import requests
from requests.auth import HTTPBasicAuth
import config

def create_xendit_qris(amount, ref_id):
    url = config.XENDIT_URL_GENERATE
    
    # Payload yang wajib dikirim ke Xendit QR Codes API
    payload = {
        "external_id": ref_id,
        "type": "DYNAMIC",
        "amount": int(amount),
        "currency": "IDR",
        "callback_url": "https://webhook.site/dummy-url"
    }
    
    # Xendit menggunakan HTTP Basic Auth dengan Secret Key sebagai username dan password kosong ("")
    auth = HTTPBasicAuth(config.XENDIT_API_KEY, "")
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        
        # Cetak log untuk debugging jika masih gagal
        print(f"[XENDIT DEBUG] Create QR Status: {response.status_code}")
        print(f"[XENDIT DEBUG] Create QR Response: {response.text}")
        
        if response.status_code in [200, 201]:
            return response.json()
        return None
    except Exception as e:
        print(f"[XENDIT ERROR] create_xendit_qris: {e}")
        return None

def check_xendit_status(ref_id):
    # Endpoint pengecekan status QR Code Xendit berdasarkan external_id
    url = f"{config.XENDIT_URL_STATUS}/{ref_id}"
    auth = HTTPBasicAuth(config.XENDIT_API_KEY, "")
    
    try:
        response = requests.get(url, auth=auth)
        
        print(f"[XENDIT DEBUG] Check Status Code: {response.status_code}")
        print(f"[XENDIT DEBUG] Check Response: {response.text}")
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"[XENDIT ERROR] check_xendit_status: {e}")
        return None