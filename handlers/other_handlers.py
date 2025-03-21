from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon_ru import LEXICON_RU


router = Router()

# Обработчик для всех сообщений что не попадают в user_handlers.
@router.message()
async def send_echo(message: Message):
    await message.reply(text=LEXICON_RU['send_echo'])
