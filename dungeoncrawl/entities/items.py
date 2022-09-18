from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

from entities.effects import Effect


class Loot(Protocol):
    name: str
    weight: float
    value: int


@dataclass
class Equipment:
    name: str
    weight: float = 0.1
    value: int = 1

    def __eq__(self, other) -> bool:
        if isinstance(other, Equipment):
            return (self.name == other.name and self.weight == other.weight
                    and self.value == other.value)
        return False

    def __hash__(self) -> int:
        return hash((self.name, self.weight, self.value))

    def __repr__(self) -> str:
        return f"{self.name}-{self.weight}kg-{self.value}gp"

    def __str__(self) -> str:
        return self.__repr__()


class Wearable(Equipment):
    name: str
    weight: float
    value: int
    wear_location: str
    armor_value: int


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
