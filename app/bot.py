from aiogram import Bot, Dispatcher
import config


# =====================================
# TELEGRAM BOT INSTANCE
# =====================================

bot = Bot(
    token=config.TELEGRAM_BOT_TOKEN
)


# =====================================
# DISPATCHER
# =====================================

dp = Dispatcher()