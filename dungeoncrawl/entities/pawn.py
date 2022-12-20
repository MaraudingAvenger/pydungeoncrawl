from dataclasses import dataclass
from functools import singledispatchmethod

from effects import Effects
from stats import Stats


@dataclass
class Point:
    x: int
    y: int


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
    
    #######################
    # ~~~ Measurements ~~~#
    #######################
    @singledispatchmethod
    def distance_to(self, other: 'Pawn') -> float:
        return ((self.position.x - other.position.x) ** 2 + (self.position.y - other.position.y) ** 2) ** 0.5
    @distance_to.register
    def _(self, other: Point) -> float:
        return ((self.position.x - other.x) ** 2 + (self.position.y - other.y) ** 2) ** 0.5
    @distance_to.register
    def _(self, x:int, y:int) -> float:
        return ((self.position.x - x) ** 2 + (self.position.y - y) ** 2) ** 0.5

    @singledispatchmethod
    def distance_from(self, other: 'Pawn') -> float:
        return self.distance_to(other)
    @distance_from.register
    def _(self, other: Point) -> float:
        return self.distance_to(other)
    @distance_from.register
    def _(self, x:int, y:int) -> float:
        return self.distance_to(x, y)
    
    
    ###################
    # ~~~ Movement ~~~#
    ###################
    @singledispatchmethod
    def move_to(self, x: int, y: int) -> None:
        self.position = Point(x, y)
    @move_to.register
    def _(self, point: Point) -> None:
        self.position = point

    def move_right(self) -> None:
        self.position.x += 1

    def move_left(self) -> None:
        self.position.x -= 1

    def move_up(self) -> None:
        self.position.y += 1

    def move_down(self) -> None:
        self.position.y -= 1

    #################
    # ~~~ Status ~~~#
    #################
    @property
    def alive(self) -> bool:
        return self.health > 0

    def take_damage(self, damage: int) -> None:
        #TODO: consider reflecting damage
        #TODO: make this work with effects
        pass

if __name__ == '__main__':
    import random

    a = Pawn('a', Point(random.randint(0,10), random.randint(0,10)), 100)
    b = Pawn('b', Point(random.randint(0,10), random.randint(0,10)), 100)
    # testing creation
    print("\nPawns:")
    print(f"a: {a.name} at {a.position}")
    print(f"b: {b.name} at {b.position}")

    # testing measurements
    print("\nCalculations:")
    print(f"distance from a -> b: ", a.distance_to(b))
    print(f"distance from a -> (2, 2): ", a.distance_to(2, 2))

    # testing movement
    print("\nMovement:")
    print(f"moving a to (2, 2)")
    a.move_to(Point(2, 2))
    print(f"a: {a.name} at {a.position}")
    print(f"moving a to (3, 3)")
    a.move_to(3, 3)
    print(f"moving down")
    a.move_down()
    print(f"a: {a.name} at {a.position}")
    print("moving left")
    a.move_left()
    print(f"a: {a.name} at {a.position}")

