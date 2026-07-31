import hashlib
import requests
import logging

import config



BASE_URL = "https://api.digiflazz.com/v1"



class DigiFlazzService:


    def __init__(self):

        self.username = config.DIGIFLAZZ_USERNAME
        self.api_key = config.DIGIFLAZZ_API_KEY



    # ==================================
    # CREATE SIGN
    # ==================================

    def _create_sign(self, ref_id):


        sign_string = (

            self.username.strip()

            +

            self.api_key.strip()

            +

            str(ref_id).strip()

        )


        return hashlib.md5(

            sign_string.encode("utf-8")

        ).hexdigest()





    # ==================================
    # REQUEST HELPER
    # ==================================

    def _post(self, endpoint, payload):


        try:


            response = requests.post(

                f"{BASE_URL}/{endpoint}",

                json=payload,

                timeout=30

            )


            print("==============================")
            print("[DIGIFLAZZ REQUEST]")
            print(payload)
            print("==============================")


            print(response.text)



            if response.status_code != 200:


                return None



            return response.json()



        except Exception as e:


            logging.error(

                f"DIGIFLAZZ ERROR : {e}"

            )


            return None






    # ==================================
    # PRICE LIST PREPAID
    # ==================================

    def prepaid_price_list(self):


        payload = {


            "cmd":
            "prepaid",


            "username":
            self.username,


            "sign":
            self._create_sign(
                "pricelist"
            )


        }



        result = self._post(

            "price-list",

            payload

        )


        if result:

            return result.get(

                "data",

                []

            )


        return []







    # ==================================
    # PRICE LIST PASCA
    # ==================================

    def pasca_price_list(self):


        payload = {


            "cmd":
            "pasca",


            "username":
            self.username,


            "sign":
            self._create_sign(
                "pricelist"
            )


        }



        result = self._post(

            "price-list",

            payload

        )


        if result:

            return result.get(

                "data",

                []

            )


        return []








    # ==================================
    # TRANSAKSI PREPAID
    # ==================================

    def prepaid_transaction(

        self,

        customer_no,

        buyer_sku_code,

        ref_id

    ):



        payload = {


            "username":
            self.username,


            "buyer_sku_code":
            buyer_sku_code,


            "customer_no":
            str(customer_no),


            "ref_id":
            ref_id,


            "sign":
            self._create_sign(ref_id)

        }




        return self._post(

            "transaction",

            payload

        )








    # ==================================
    # CEK TAGIHAN PASCA
    # ==================================

    def inquiry_pasca(

        self,

        customer_no,

        buyer_sku_code,

        ref_id

    ):


        payload = {


            "commands":
            "inq-pasca",


            "username":
            self.username,


            "buyer_sku_code":
            buyer_sku_code,


            "customer_no":
            str(customer_no),


            "ref_id":
            ref_id,


            "sign":
            self._create_sign(ref_id)


        }




        return self._post(

            "transaction",

            payload

        )








    # ==================================
    # BAYAR PASCA
    # ==================================

    def pay_pasca(

        self,

        customer_no,

        buyer_sku_code,

        ref_id

    ):


        payload = {


            "commands":
            "pay-pasca",


            "username":
            self.username,


            "buyer_sku_code":
            buyer_sku_code,


            "customer_no":
            str(customer_no),


            "ref_id":
            ref_id,


            "sign":
            self._create_sign(ref_id)


        }



        return self._post(

            "transaction",

            payload

        )







    # ==================================
    # AMBIL STATUS
    # ==================================

    def get_status(

        self,

        response

    ):


        try:


            data = response.get(

                "data",

                {}

            )


            return str(

                data.get(

                    "status",

                    ""

                )

            ).upper()



        except:


            return ""





    # ==================================
    # AMBIL SN
    # ==================================

    def get_sn(

        self,

        response

    ):


        try:


            data = response.get(

                "data",

                {}

            )


            return (

                data.get("sn")

                or

                data.get("serial_number")

            )


        except:


            return None






digiflazz = DigiFlazzService()