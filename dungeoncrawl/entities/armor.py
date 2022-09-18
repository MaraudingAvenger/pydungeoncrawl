from dataclasses import dataclass, field

from dungeoncrawl.entities.items import Wearable
from dungeoncrawl.entities.effects import Effect


@dataclass
class Clothing(Wearable):
    name = "Clothes"
    weight = 1
    value = 1
    armor_value = 1
    effects: list[Effect] = field(default_factory=list)
