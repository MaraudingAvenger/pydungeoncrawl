from collections import namedtuple
from typing import NamedTuple

from dungeoncrawl.entities.effects import Effects
from dungeoncrawl.entities.stats import Stats

Point = namedtuple('Coord', ['x', 'y'])

class Pawn:
    name: str
    position: NamedTuple
    effects: Effects
    stats: Stats
    health_max: int
    health: int

    def __init__(self, name, position: tuple[int,int] | None = None) -> None:
        self.name = name
        if position is not None:
            self.position = Point(x=position[0], y=position[1])
        else:
            self.position = Point(x=0, y=0)


    @property
    def has_effects(self) -> bool:
        return self.effects.active

    @property
    def alive(self) -> bool:
        return self.health > 0

    def move_to(self, x:int, y:int) -> None:
        self.position = Point(x, y)

    def move_left(self) -> None:
        self.position = Point(self.position.x-1, self.position.y)

    def move_right(self) -> None:
        self.position = Point(self.position.x+1, self.position.y)

    def move_up(self) -> None:
        self.position = Point(self.position.x, self.position.y+1)

    def move_down(self) -> None:
        self.position = Point(self.position.x, self.position.y-1)

    