import requests


URL = "http://127.0.0.1:8000/transactions/buy"


PARAMS = {

    "telegram_id": "1111111",

    "buyer_sku_code": "ax50",

    "customer_no": "08123456789"

}


print("==============================")
print("TEST TRANSACTION")
print("==============================")


response = requests.post(
    URL,
    params=PARAMS
)


print("==============================")
print("STATUS CODE")
print(response.status_code)

print("==============================")
print("RESPONSE")
print(response.text)

print("==============================")