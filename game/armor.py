from dataclasses import dataclass, field
from game.things import Wearable
from game.effects import Effect


@dataclass
class Clothing(Wearable):
    name = "Clothes"
    weight = 1
    value = 1
    armor_value = 1
    effects: list[Effect] = field(default_factory=list)
