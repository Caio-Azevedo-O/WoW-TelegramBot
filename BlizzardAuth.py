import requests
from time import time
from os import getenv

class BlizzardAuth:
    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id or getenv("BLIZZARD_CLIENT_ID")
        self.client_secret = client_secret or getenv("BLIZZARD_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            raise ValueError("Client ID e Client Secret da Blizzard são obrigatórios.")

        self.token = None
        self.token_expires_at = 0

        self.session = requests.Session()

        self.base_url = "https://us.api.blizzard.com"
        
    def getAccessToken(self):
        if self.token and time() < self.token_expires_at:
            return self.token

        response = self.session.post(
            "https://oauth.battle.net/token",
            auth=(self.client_id, self.client_secret),
            data={"grant_type": "client_credentials"},
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        self.token = data["access_token"]
        self.token_expires_at = (
            time() + data["expires_in"] - 60
        )

        return self.token
    def getHeaders(self):
        return {
            "Authorization": f"Bearer {self.getAccessToken()}"
        }