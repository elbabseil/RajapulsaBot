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

    def _create_sign(
        self,
        ref_id
    ):

        raw = (

            self.username.strip()
            +
            self.api_key.strip()
            +
            str(ref_id).strip()

        )


        return hashlib.md5(
            raw.encode("utf-8")
        ).hexdigest()





    # ==================================
    # REQUEST DIGIFLAZZ
    # ==================================

    def _post(
        self,
        endpoint,
        payload
    ):


        try:


            print("==============================")
            print("DIGIFLAZZ URL")
            print(
                f"{BASE_URL}/{endpoint}"
            )


            print("DIGIFLAZZ PAYLOAD")
            print(payload)

            print("==============================")



            response = requests.post(

                f"{BASE_URL}/{endpoint}",

                json=payload,

                timeout=30

            )



            print("==============================")
            print("HTTP STATUS")
            print(response.status_code)

            print("DIGIFLAZZ RESPONSE")
            print(response.text)

            print("==============================")




            try:

                return response.json()



            except Exception:


                return {

                    "error": response.text,

                    "status_code": response.status_code

                }





        except Exception as e:


            logging.error(
                f"DIGIFLAZZ ERROR : {e}"
            )


            print("==============================")
            print("REQUEST ERROR")
            print(e)
            print("==============================")


            return {

                "error": str(e)

            }






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
            self._create_sign(
                ref_id
            )

        }




        return self._post(

            "transaction",

            payload

        )








    # ==================================
    # INQUIRY PASCA
    # ==================================

    def inquiry_pasca(
        self,
        customer_no,
        buyer_sku_code,
        ref_id
    ):


        payload = {


            "cmd":
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
            self._create_sign(
                ref_id
            )

        }



        return self._post(

            "transaction",

            payload

        )








    # ==================================
    # BAYAR PASCA
    # ==================================

    def pasca_transaction(
        self,
        customer_no,
        buyer_sku_code,
        ref_id
    ):


        payload = {


            "cmd":
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
            self._create_sign(
                ref_id
            )

        }



        return self._post(

            "transaction",

            payload

        )







    # ==================================
    # GET STATUS
    # ==================================

    def get_status(
        self,
        response
    ):


        try:


            return str(

                response
                .get(
                    "data",
                    {}
                )
                .get(
                    "status",
                    ""
                )

            ).upper()



        except:


            return ""








    # ==================================
    # GET MESSAGE
    # ==================================

    def get_message(
        self,
        response
    ):


        try:


            return response.get(

                "data",

                {}

            ).get(

                "message",

                ""

            )



        except:


            return ""








    # ==================================
    # GET SN
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







    # ==================================
    # CEK SALDO
    # ==================================

    def check_balance(self):


        payload = {


            "cmd":
            "deposit",


            "username":
            self.username,


            "sign":
            self._create_sign(
                "depo"
            )

        }



        return self._post(

            "cek-saldo",

            payload

        )







digiflazz = DigiFlazzService()