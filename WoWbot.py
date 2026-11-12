import requests as r
from os import getenv
from time import time
from dotenv import load_dotenv as load

TelegramToken = getenv("TELEGRAM_API_KEY")
WoWClientID = getenv("WOW_CLIENT_ID")
WoWClientSecret = getenv("WOW_CLIENT_SECRET")

WowApiUrl = f'https://'
BotApiUrl = f'https://telegram.org/bot{TelegramToken}'

def main()