import requests
import config


XENDIT_QRIS_URL = "https://api.xendit.co/qr_codes"


class XenditService:


    def __init__(self):

        self.api_key = config.XENDIT_API_KEY

        self.callback_url = config.XENDIT_CALLBACK_URL



    def headers(self):

        return {

            "Content-Type": "application/json"

        }



    # ==============================
    # CREATE QRIS
    # ==============================

    def create_qris(
        self,
        external_id,
        amount
    ):


        payload = {

            "external_id": external_id,

            "type": "DYNAMIC",

            "amount": amount,

            "callback_url": self.callback_url

        }



        try:


            response = requests.post(

                XENDIT_QRIS_URL,

                auth=(

                    self.api_key,

                    ""

                ),

                headers=self.headers(),

                json=payload,

                timeout=30

            )


            print("==============================")
            print("[XENDIT CREATE QRIS]")
            print(response.text)
            print("==============================")


            return response.json()



        except Exception as e:


            print(
                "[XENDIT CREATE ERROR]",
                e
            )


            return None





    # ==============================
    # CHECK QRIS STATUS
    # ==============================

    def get_qris_status(
        self,
        qr_id
    ):


        url = (

            f"{XENDIT_QRIS_URL}/{qr_id}"

        )



        try:


            response = requests.get(

                url,

                auth=(

                    self.api_key,

                    ""

                ),

                headers=self.headers(),

                timeout=30

            )


            print("==============================")
            print("[XENDIT STATUS]")
            print(response.text)
            print("==============================")


            return response.json()



        except Exception as e:


            print(

                "[XENDIT STATUS ERROR]",

                e

            )


            return None




xendit = XenditService()