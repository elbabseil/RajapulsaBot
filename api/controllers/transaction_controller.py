from app.services.transaction_service import transaction_service
from app.database.product_repository import product_repository



def buy_product(
    telegram_id,
    buyer_sku_code,
    customer_no
):

    print("==============================")
    print("CONTROLLER BUY MASUK")
    print("telegram_id :", telegram_id)
    print("buyer_sku_code :", buyer_sku_code)
    print("customer_no :", customer_no)
    print("==============================")


    try:

        products = product_repository.get_all()


        print("==============================")
        print("TOTAL PRODUK :", len(products))
        print("==============================")


        product = None


        for item in products:


            sku = str(
                item.get("buyer_sku_code")
            ).strip()


            request_sku = str(
                buyer_sku_code
            ).strip()



            if sku.lower() == request_sku.lower():


                product = item

                break




        if product is None:


            print("==============================")
            print("PRODUK TIDAK DITEMUKAN")
            print("SKU :", buyer_sku_code)
            print("==============================")


            return {


                "success": False,


                "message": "Produk tidak ditemukan",


                "sku": buyer_sku_code


            }





        print("==============================")
        print("PRODUK DITEMUKAN")
        print(product)
        print("==============================")




        result = transaction_service.buy_product(

            telegram_id,

            product,

            customer_no

        )



        return result





    except Exception as e:


        print("==============================")
        print("ERROR CONTROLLER BUY")
        print(e)
        print("==============================")


        return {


            "success": False,


            "message": str(e)


        }