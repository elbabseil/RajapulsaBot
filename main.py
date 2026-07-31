import asyncio

from app.loader import (
    bot,
    dp,
    startup
)


async def main():

    startup()

    print("[BOT] RajaPulsa Bot berjalan...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())