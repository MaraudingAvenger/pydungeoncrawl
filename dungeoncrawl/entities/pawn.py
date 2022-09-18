from abc import ABC, abstractmethod
from dungeoncrawl.entities.effects import Effects
from dungeoncrawl.entities.stats import Stats


class Pawn(ABC):
    name: str
    position: tuple[int]
    effects: Effects
    stats: Stats
    health_max: int
    health: int

    @property
    def has_effects(self) -> bool:
        return self.effects.active

    @property
    def alive(self) -> bool:
        return self.health > 0

    @abstractmethod
    def move(self, x: int, y: int) -> None:
        ...
