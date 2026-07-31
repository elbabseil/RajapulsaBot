from app.bot import bot, dp

from app.routers import register_routers

from app.database.transaction_repository import transaction_repository

from worker.payment_worker import payment_worker



def startup():

    print("==============================")
    print(" RAJAPULSA STARTUP ")
    print("==============================")


    try:

        transaction_repository.create_table()

        print("[DATABASE] OK")


    except Exception as e:

        print("[DATABASE ERROR]", e)



    try:

        payment_worker.start()

        print("[PAYMENT WORKER] OK")


    except Exception as e:

        print("[WORKER ERROR]", e)



    register_routers(dp)

    print("[ROUTER] OK")



    