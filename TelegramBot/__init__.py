import os
from dotenv import load_dotenv
import logging

from aiogram import Bot, Dispatcher, executor, types

load_dotenv()

HTTP_API_BOT_TOKEN = os.getenv('HTTP_API_BOT_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token = HTTP_API_BOT_TOKEN)
dp = Dispatcher(bot)