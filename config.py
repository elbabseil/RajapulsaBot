from dotenv import load_dotenv
import os


load_dotenv()



def get_env(name):

    value = os.getenv(name)

    if not value:

        raise RuntimeError(
            f"{name} belum diatur"
        )

    return value



GEMINI_API_KEY = get_env(
    "GEMINI_API_KEY"
)


DIGIFLAZZ_API_KEY = get_env(
    "DIGIFLAZZ_API_KEY"
)


DIGIFLAZZ_USERNAME = get_env(
    "DIGIFLAZZ_USERNAME"
)


XENDIT_API_KEY = get_env(
    "XENDIT_API_KEY"
)


XENDIT_CALLBACK_URL = get_env(
    "XENDIT_CALLBACK_URL"
)


TELEGRAM_BOT_TOKEN = get_env(
    "TELEGRAM_BOT_TOKEN"
)