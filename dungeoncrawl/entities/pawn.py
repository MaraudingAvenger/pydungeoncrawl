from collections import namedtuple
from typing import NamedTuple

from dungeoncrawl.entities.effects import Effects
from dungeoncrawl.entities.stats import Stats

Point = namedtuple('Point', ['x', 'y'])


class Pawn:
    name: str
    position: Point
    effects: Effects
    stats: Stats
    health_max: int
    health: int

    def __init__(self,
                 name,
                 position: Point | tuple[int, int],
                 health_max: int) -> None:
        self.name = name
        self.position = position if isinstance(
            position, Point) else Point(*position)
        self.health_max = health_max
        self.health = self.health_max

    @property
    def has_effects(self) -> bool:
        return self.effects.active

    @property
    def alive(self) -> bool:
        return self.health > 0

    def move_to(self, x: int, y: int) -> None:
        self.position = Point(x, y)

    def move_left(self) -> None:
        self.position = Point(self.position.x-1, self.position.y)

    def move_right(self) -> None:
        self.position = Point(self.position.x+1, self.position.y)

    def move_up(self) -> None:
        self.position = Point(self.position.x, self.position.y+1)

    def move_down(self) -> None:
        self.position = Point(self.position.x, self.position.y-1)
