from dataclasses import dataclass, field
import random

from dungeoncrawl.entities.items import Weapon
from dungeoncrawl.entities.effects import Effect, Fire


@dataclass
class Fist(Weapon):
    name: str = field(default="fist", init=False)
    weight: float = field(default=0, init=False)
    value: int = field(default=0, init=False)
    min_dmg: int = field(default=1, init=False)
    max_dmg: int = field(default=4, init=False)

    def deal_damage(self) -> int:
        return random.randint(self.min_dmg, self.max_dmg)


@dataclass
class Sword(Weapon):
    name: str = field(default="generic sword")
    weight: float = field(default=3.0, init=False)
    value: int = field(default=5, init=False)
    min_dmg: int = field(default=1, init=False)
    max_dmg: int = field(default=6, init=False)

    def deal_damage(self) -> int:
        return random.randint(self.min_dmg, self.max_dmg)


@dataclass
class FireSword(Weapon):
    '''
    Magic sword that does 2 points of fire damage with each strike.
    '''
    name: str = field(default="sword+1")
    weight: float = field(default=2.5, init=False)
    value: int = field(default=25, init=False)
    min_dmg: int = field(default=2, init=False)
    max_dmg: int = field(default=7, init=False)
    magic_effect: Effect = Effect("fire", 2)

    def deal_damage(self) -> int:
        return random.randint(self.min_dmg, self.max_dmg) + self.magic_effect.bonus_damage
