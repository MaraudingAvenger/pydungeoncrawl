from dataclasses import dataclass
from functools import singledispatchmethod

from effects import Effects


@dataclass
class Point:
    x: int
    y: int


class Pawn:
    name: str
    position: Point
    effects: Effects
    health_max: int
    health: int

    def __init__(self,
                 name,
                 position: Point | tuple[int, int],
                 health_max: int) -> None:
        self.name = name
        self.position = position if isinstance(
            position, Point) else Point(*position)
        self.facing_direction = Point(0, 0)
        self.health_max = health_max
        self.health = self.health_max

    @property
    def has_effects(self) -> bool:
        return self.effects.active

    ########################
    # ~~~ Measurements ~~~ #
    ########################
    @singledispatchmethod
    def distance_to(self, other: 'Pawn') -> float:
        return ((self.position.x - other.position.x) ** 2 + (self.position.y - other.position.y) ** 2) ** 0.5

    @distance_to.register
    def _(self, other: Point) -> float:
        return ((self.position.x - other.x) ** 2 + (self.position.y - other.y) ** 2) ** 0.5

    @distance_to.register
    def _(self, x: int, y: int) -> float:
        return ((self.position.x - x) ** 2 + (self.position.y - y) ** 2) ** 0.5

    @singledispatchmethod
    def distance_from(self, other: 'Pawn') -> float:
        return self.distance_to(other)

    @distance_from.register
    def _(self, other: Point) -> float:
        return self.distance_to(other)

    @distance_from.register
    def _(self, x: int, y: int) -> float:
        return self.distance_to(x, y)

    ####################
    # ~~~ Movement ~~~ #
    ####################

    @singledispatchmethod
    def move_to(self, x: int, y: int) -> None:
        if self.distance_from(x, y) > 1.5:
            self.position = Point(x, y)
            return

        self.facing_direction = Point(
            x+(x-self.position.x), y+(y-self.position.y))
        self.position = Point(x, y)

    @move_to.register
    def _(self, point: Point) -> None:
        self.move_to(point.x, point.y)

    @singledispatchmethod
    def face(self, target: 'Pawn') -> None:
        self.facing_direction = target.position

    @face.register
    def _(self, target: Point) -> None:
        self.facing_direction = target

    @face.register
    def _(self, x: int, y: int) -> None:
        self.facing_direction = Point(x, y)

    def move_right(self) -> None:
        self.position.x += 1

    def move_left(self) -> None:
        self.position.x -= 1

    def move_up(self) -> None:
        self.position.y += 1

    def move_down(self) -> None:
        self.position.y -= 1

    ##################
    # ~~~ Status ~~~ #
    ##################
    @property
    def alive(self) -> bool:
        return self.health > 0

    ##################
    # ~~~ Combat ~~~ #
    ##################
    def take_damage(self, damage: int) -> None:
        pct_extra_damage = damage * self.effects.bonus_damage_received_percent
        num_extra_damage = self.effects.bonus_damage_received

        dmg = damage + int(round(pct_extra_damage, 0)) + num_extra_damage
        
        if dmg > 0:
            self.health -= dmg
            self.was_hit = True

    def heal(self, amount: int) -> None:
        self.health += amount
        if self.health > self.health_max:
            self.health = self.health_max


if __name__ == '__main__':
    import random

    a = Pawn('a', Point(random.randint(0, 10), random.randint(0, 10)), 100)
    b = Pawn('b', Point(random.randint(0, 10), random.randint(0, 10)), 100)
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
