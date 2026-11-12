from BlizzardAuth import BlizzardAuth
from difflib import SequenceMatcher
from Queries.WoWItemSearchQuery import WoWItemSearchQuery
from Dtos.WoWItemDto import WoWItemDto

class WoWItemSearch:
    def __init__(self, blizzardAuth: BlizzardAuth):
        self.blizzardAuth = blizzardAuth

    def _matchName(self, search_text: str, search_item: str) -> float:
        return SequenceMatcher(None, search_text.lower(), search_item.lower()).ratio()

    def searchItem(self, itemSearchQuery: WoWItemSearchQuery) -> list[WoWItemDto]:
        url = f"{self.blizzardAuth.base_url}/data/wow/search/item"

        params = {
            "namespace": "static-us",
            "name.pt_BR": itemSearchQuery.name,
            "_pageSize": 100
        }

        response = self.blizzardAuth.session.get(
            url,
            headers = self.blizzardAuth.getHeaders(),
            params = params,
            timeout = 30
        )

        response.raise_for_status()

        results = response.json().get("results", [])
        
        sortedResults = sorted(
            results,
            key=lambda item: self._matchName(
                itemSearchQuery.name,
                item["data"]["name"].get("pt_BR", "")
            ),
            reverse=True
        )

        topResults = []
        for item in sortedResults[:10]:
            data = item["data"]
            dto = WoWItemDto(
                item_name=data["name"].get("pt_BR", "Sem nome"),
                item_quality=data.get("quality", {}).get("name", {}).get("pt_BR", "Desconhecida"),
                item_level=data.get("level", 0),
                item_class=data.get("item_class", {}).get("name", {}).get("pt_BR", "N/A"),
                item_subclass=data.get("item_subclass", {}).get("name", {}).get("pt_BR", "N/A")
            )
            topResults.append(dto)

        return topResults