from app.services.product_service import product_service


def get_all_products():

    products = product_service.get_all_products()

    return {
        "success": True,
        "total": len(products),
        "data": products
    }



def get_prepaid_products():

    products = product_service.get_prepaid_products()

    return {
        "success": True,
        "total": len(products),
        "data": products
    }



def get_pasca_products():

    products = product_service.get_pasca_products()

    return {
        "success": True,
        "total": len(products),
        "data": products
    }



def sync_products():

    result = product_service.sync()

    return {
        "success": True,
        "message": "Sinkronisasi berhasil",
        "result": result
    }