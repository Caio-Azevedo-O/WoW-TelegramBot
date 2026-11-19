from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class WoWItemDto:
    item_name: str
    item_quality: str 
    item_level: int
    item_class: str
    item_subclass: str