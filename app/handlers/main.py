import asyncio
import logging

from aiogram import Bot, Dispatcher

import config

from app.routers import register_routers

from app.database.transaction_repository import (
    transaction_repository
)

from app.workers.payment_worker import (
    payment_worker
)


bot = Bot(
    token=config.TELEGRAM_BOT_TOKEN
)


dp = Dispatcher()


async def main():

    logging.basicConfig(
        level=logging.INFO
    )


    print("==============================")
    print(" RajaPulsa Bot Starting ")
    print("==============================")


    # database
    transaction_repository.create_table()

    print(
        "[SYSTEM] Database siap"
    )


    # worker pembayaran
    payment_worker.start()

    print(
        "[SYSTEM] Payment Worker aktif"
    )


    # register handler
    register_routers(dp)


    print(
        "[SYSTEM] Router aktif"
    )


    await dp.start_polling(
        bot
    )



if __name__ == "__main__":

    asyncio.run(
        main()
    )