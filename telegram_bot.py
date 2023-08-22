import os
from dotenv import load_dotenv

load_dotenv() 
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(bot, message):
    for chat_id in TELEGRAM_CHAT_ID:
        if chat_id:
            bot.send_message(chat_id, message)
        else:
            print("Invalid chat ID:", chat_id)
