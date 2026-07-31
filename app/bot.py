from aiogram import Bot, Dispatcher
import config


bot = Bot(
    config.TELEGRAM_BOT_TOKEN
)


dp = Dispatcher()