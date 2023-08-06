from dataclasses import dataclass

@dataclass
class Item():
    name: str
    desc: str
    builds_into: list
    buy_price: int
    sell_price: int
    tags: list
    effects: dict