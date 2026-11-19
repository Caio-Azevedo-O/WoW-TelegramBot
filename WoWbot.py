import requests
from os import getenv
from dotenv import load_dotenv

from BlizzardAuth import BlizzardAuth
from WoWItemSearchApi import WoWItemSearch
from Queries.WoWItemSearchQuery import WoWItemSearchQuery

load_dotenv()

TOKEN = getenv("TELEGRAM_API_KEY")
URL = f"https://api.telegram.org/bot{TOKEN}"

blizzard = BlizzardAuth()
wow = WoWItemSearch(blizzard)

offset = 0

print("Bot iniciado!")

while True:

    updates = requests.get(
        f"{URL}/getUpdates",
        params={"offset": offset, "timeout": 30}
    ).json()["result"]

    for update in updates:

        offset = update["update_id"] + 1

        message = update.get("message")

        if not message or "text" not in message:
            continue

        chat_id = message["chat"]["id"]
        text = message["text"]

        if text == "/start":
            resposta = "Olá! Envie o nome de um item do WoW."
        
        else:
            query = WoWItemSearchQuery(name=text)
            items = wow.searchItem(query)

            resposta = ""

            for item in items:
                resposta += (
                    f"Nome: {item.item_name}\n"
                    f"Qualidade: {item.item_quality}\n"
                    f"Nível: {item.item_level}\n"
                    f"Classe: {item.item_class}\n"
                    f"Subclasse: {item.item_subclass}\n"
                    f"--------------------\n"
                )

            if not resposta:
                resposta = "Nenhum item encontrado."

        requests.post(
            f"{URL}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": resposta
            }
        )