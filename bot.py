import asyncio
from aiogram import executor

from bot_init import dp
from Handlers import messages, Flatty

messages.register_message_handlers(dp)
Flatty.register_message_handlers(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
