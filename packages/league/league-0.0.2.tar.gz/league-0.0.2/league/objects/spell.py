from dataclasses import dataclass

@dataclass
class Spell():
    name: str
    desc: str
    cooldown: int
    cost: int
    required_level: int
    effect_range: int