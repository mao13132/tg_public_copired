from aiogram import Dispatcher
from aiogram.types import Message


async def start(message: Message):
    await message.answer(message.text)


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, text_contains='')
