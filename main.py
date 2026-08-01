import asyncio

from app.loader import (
    bot,
    dp,
    startup
)

from app.database.migration import migrate_orders

from app.services.workers.payment_worker import payment_worker
from app.services.workers.status_worker import status_worker



async def main():


    print(
        "[DATABASE MIGRATION] CHECK..."
    )


    migrate_orders()


    startup()



    print(
        "[PAYMENT WORKER] STARTING..."
    )


    asyncio.create_task(
        payment_worker.start()
    )


    print(
        "[PAYMENT WORKER] OK"
    )



    print(
        "[STATUS WORKER] STARTING..."
    )


    asyncio.create_task(
        status_worker.start()
    )


    print(
        "[STATUS WORKER] OK"
    )



    print(
        "[BOT] RajaPulsa Bot berjalan..."
    )


    await dp.start_polling(bot)




if __name__ == "__main__":

    asyncio.run(main())