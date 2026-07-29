from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DIGIFLAZZ_API_KEY = os.getenv("DIGIFLAZZ_API_KEY")
DIGIFLAZZ_USERNAME = os.getenv("DIGIFLAZZ_USERNAME")
XENDIT_API_KEY = os.getenv("XENDIT_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")