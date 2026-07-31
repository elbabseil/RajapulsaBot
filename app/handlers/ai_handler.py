from aiogram import Router, types

from app.handlers.ai import process_ai_message


router = Router()


@router.message()
async def ai_handler(
    message: types.Message
):

    await process_ai_message(
        message
    )