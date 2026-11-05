import requests as r
from os import getenv
from dotenv import load_dotenv as load

TelegramToken = getenv("TELEGRAM_API_KEY")
WoWApiToken = getenv("WOW_API_KEY")

WowApiUrl = f'https://'
BotApiUrl = f'https://telegram.org/bot{TelegramToken}'