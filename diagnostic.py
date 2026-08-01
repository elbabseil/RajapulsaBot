import sys
import os


PASS = "[✓]"
FAIL = "[✗]"
WARN = "[!]"


def title(text):

    print("\n" + "=" * 45)
    print(text)
    print("=" * 45)



def check(name, function):

    try:

        result = function()

        if result:

            print(f"{PASS} {name}")
            return True

        else:

            print(f"{FAIL} {name}")
            return False


    except Exception as e:

        print(f"{FAIL} {name}")
        print(f"     Error: {e}")

        return False



# =====================================
# PYTHON
# =====================================

def check_python():

    print(
        f"     Python : {sys.version.split()[0]}"
    )

    print(
        f"     Path   : {sys.executable}"
    )

    return sys.version_info.major >= 3



# =====================================
# VIRTUAL ENV
# =====================================

def check_venv():

    return (
        hasattr(sys, "base_prefix")
        and
        sys.prefix != sys.base_prefix
    )



# =====================================
# ENV FILE
# =====================================

def check_env():

    return os.path.exists(
        ".env"
    )



# =====================================
# CONFIG
# =====================================

def check_config():

    import config

    return True



# =====================================
# DATABASE
# =====================================

def check_database():

    from app.database.order_repository import order_repository

    order_repository.create_table()

    return True



# =====================================
# PRODUCTS
# =====================================

def check_products():

    from app.services.product_service import get_products


    products = get_products()


    print(
        f"     Products loaded : {len(products)}"
    )


    return len(products) > 0



# =====================================
# ORDER SERVICE
# =====================================

def check_order_service():

    from app.services.order_service import order_service


    return order_service is not None



# =====================================
# DIGIFLAZZ
# =====================================

def check_digiflazz():

    import config


    username = getattr(
        config,
        "DIGIFLAZZ_USERNAME",
        None
    )


    api_key = getattr(
        config,
        "DIGIFLAZZ_API_KEY",
        None
    )


    return bool(
        username
        and
        api_key
    )



# =====================================
# FASTAPI
# =====================================

def check_fastapi():

    import api


    return api.app is not None



# =====================================
# TELEGRAM
# =====================================

def check_telegram():

    import config


    token = getattr(
        config,
        "TELEGRAM_BOT_TOKEN",
        None
    )


    return bool(token)



# =====================================
# MAIN
# =====================================

def main():


    title(
        "RAJAPULSABOT DIAGNOSTIC v1.1"
    )


    result = []


    result.append(
        check(
            "Python Version",
            check_python
        )
    )


    result.append(
        check(
            "Virtual Environment",
            check_venv
        )
    )


    result.append(
        check(
            ".env File",
            check_env
        )
    )


    result.append(
        check(
            "Config",
            check_config
        )
    )


    result.append(
        check(
            "Database",
            check_database
        )
    )


    result.append(
        check(
            "Product Repository",
            check_products
        )
    )


    result.append(
        check(
            "Order Service",
            check_order_service
        )
    )


    result.append(
        check(
            "DigiFlazz Config",
            check_digiflazz
        )
    )


    result.append(
        check(
            "FastAPI",
            check_fastapi
        )
    )


    result.append(
        check(
            "Telegram Token",
            check_telegram
        )
    )


    title(
        "RESULT"
    )


    if all(result):

        print(
            "SYSTEM READY"
        )

    else:

        print(
            "SYSTEM HAS PROBLEMS"
        )


    print()



if __name__ == "__main__":

    main()