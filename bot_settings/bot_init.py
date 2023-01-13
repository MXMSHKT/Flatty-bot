import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)
file = open('API_TOKEN.txt')
API_TOKEN = [x.strip() for x in file.readlines()]
# API_TOKEN = os.environ.get(BOT_TOKEN)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN[0])
dp = Dispatcher(bot, storage=storage)
