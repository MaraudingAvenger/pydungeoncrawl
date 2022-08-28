from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random

from game.effects import Effect
from game.things import Equipment

class Weapon(ABC, Equipment):
    name: str
    weight: float
    value: int
    min_dmg: int
    max_dmg: int
    effects: list[Effect]

    @abstractmethod
    def deal_damage(self) -> int:
        ...

    def __hash__(self) -> int:
        return hash((self.name, self.weight, self.min_dmg, self.max_dmg))

    def __repr__(self) -> str:
        return f"{self.name}-{self.weight} kg-{(self.max_dmg + self.min_dmg)/2} avg dmg"

    def __str__(self) -> str:
        return self.__repr__()

@dataclass
class Fist(Weapon):
    name:str = field(default="fist",init=False)
    weight:float = field(default=0,init=False)
    value:int = field(default=0,init=False)
    min_dmg:int = field(default=1,init=False)
    max_dmg:int = field(default=4,init=False)

    def deal_damage(self) -> int:
        return random.randint(self.min_dmg, self.max_dmg)

@dataclass
class Sword(Weapon):
    name:str = field(default="generic sword")
    weight: float = field(default=3.0,init=False)
    value:int = field(default=5,init=False)
    min_dmg:int = field(default=1,init=False)
    max_dmg:int = field(default=6,init=False)

    def deal_damage(self) -> int:
        return random.randint(self.min_dmg, self.max_dmg)