from dataclasses import dataclass

@dataclass
class Character():
    name: str
    title: str
    desc: str
    partype: str
    tags: list
    info: dict
    stats: dict