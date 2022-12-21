from dataclasses import dataclass
from functools import singledispatchmethod

from dungeoncrawl.entities.equipment import Gear, GearSet
from dungeoncrawl.entities.equipment import Equipment
from dungeoncrawl.entities.effects import Effects
from dungeoncrawl.utilities.location import Point, distance_between, behinds


@dataclass
class _Character:
    position: Point

class Pawn(_Character):

    def __init__(self,
                 name,
                 position: Point | tuple[int, int],
                 health_max: int,
                 symbol:str = '@') -> None:
        
        self.name = name
        
        # position
        self._position = position if isinstance(
            position, Point) else Point(*position)
        self.facing_direction = Point(0, 0)
        
        # status
        self.health_max = health_max
        self._health = health_max
        self._is_dead = False
        
        # effects
        self.equipment = Equipment()
        self.effects = Effects()

        # internal use
        self.move_history = []
        self.action_history = []
        self._symbol = symbol

    ####################
    # ~~~ Location ~~~ #
    ####################
    @property
    def position(self) -> Point:
        return self._position

    @position.setter
    def position(self, value: Point | tuple[int, int]) -> None:
        self._position = value if isinstance(
            value, Point) else Point(*value)
        self.move_history.append(self._position)

    @property
    def points_behind(self) -> tuple[Point,...]:
        return behinds(self.position, self.facing_direction)

    ##################
    # ~~~ Status ~~~ #
    ##################
    @property
    def has_effects(self) -> bool:
        return self.effects.active

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int) -> None:
        if not self._is_dead:
            self._health = value
            if self._health < 0:
                self._health = 0
            self._is_dead = self._health <= 0

    ########################
    # ~~~ Measurements ~~~ #
    ########################
    @singledispatchmethod
    def distance_to(self, other: _Character) -> float:
        return distance_between(self.position, other.position)
    @distance_to.register
    def _(self, other: Point) -> float:
        return distance_between(self.position, other)
    @distance_to.register
    def _(self, x: int, y: int) -> float:
        return distance_between(self.position, Point(x, y))

    @singledispatchmethod
    def distance_from(self, other: _Character) -> float:
        return self.distance_to(other)
    @distance_from.register
    def _(self, other: Point) -> float:
        return self.distance_to(other)
    @distance_from.register
    def _(self, x: int, y: int) -> float:
        return self.distance_to(x, y)

    #TODO: ALL OF THIS LOGIC IS GOING TO THE CONTROLLER
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
    def face(self, target: _Character) -> None:
        self.facing_direction = target.position
    @face.register
    def _(self, target: Point) -> None:
        self.facing_direction = target
    @face.register
    def _(self, x: int, y: int) -> None:
        self.facing_direction = Point(x, y)

    def move_down_right(self) -> None:
        self.position.x += 1
        self.position.y -= 1
        self.face(self.position.x+1, self.position.y-1)
    
    def move_right(self) -> None:
        self.position.x += 1
        self.face(self.position.x+1, self.position.y)
    
    def move_up_right(self) -> None:
        self.position.x += 1
        self.position.y += 1
        self.face(self.position.x+1, self.position.y+1)

    def move_down_left(self) -> None:
        self.position.x -= 1
        self.position.y -= 1
        self.face(self.position.x-1, self.position.y-1)
    
    def move_left(self) -> None:
        self.position.x -= 1
        self.face(self.position.x-1, self.position.y)
    
    def move_up_left(self) -> None:
        self.position.x -= 1
        self.position.y += 1
        self.face(self.position.x-1, self.position.y+1)

    def move_up(self) -> None:
        self.position.y += 1
        self.face(self.position.x, self.position.y+1)

    def move_down(self) -> None:
        self.position.y -= 1
        self.face(self.position.x, self.position.y-1)

    @singledispatchmethod
    def move_toward(self, target: Point) -> None: 
        
        # use bresenham's algorithm to pick find the next point on the line between the two points
        # https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm

        def bresenham(origin: Point, destination: Point):
            x1, y1 = origin.x, origin.y
            x2, y2 = destination.x, destination.y
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy

            while True:
                if x1 == x2 and y1 == y2:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err = err - dy
                    x1 = x1 + sx
                if e2 < dx:
                    err = err + dx
                    y1 = y1 + sy
                yield x1, y1

        if self.distance_from(target) > 1.5:
            path = bresenham(self.position, target)
            self.position = Point(*next(path))
            self.face(*next(path))
        
    @move_toward.register
    def _(self, target: _Character) -> None:
        self.move_toward(target.position)
    @move_toward.register
    def _(self, x: int, y: int) -> None:
        self.move_toward(Point(x, y))      
    

    ##################
    # ~~~ Combat ~~~ #
    ##################
    def _take_damage(self, damage: int) -> None:
        pct_extra_damage = damage * self.effects.bonus_damage_received_percent
        num_extra_damage = self.effects.bonus_damage_received

        dmg = damage + int(round(pct_extra_damage, 0)) + num_extra_damage
            
        if dmg > 0:
            self.health -= dmg
            self.was_hit = True

    def _heal(self, amount: int) -> None:
        self.health += amount
        if self.health > self.health_max:
            self.health = self.health_max

    ###############################
    # ~~~ Convenience Methods ~~~ #
    ###############################
    def equip(self, item: Gear|GearSet) -> None:
        return self.equipment.equip(item)
    def unequip(self, item: Gear|GearSet|str) -> None:
        return self.equipment.unequip(item)
    def stunned(self) -> bool:
        return self.effects.stunned
    def poisoned(self) -> bool:
        return self.effects.poisoned
    def rooted(self) -> bool:
        return self.effects.rooted
    def vulnerable(self) -> bool:
        return self.effects.vulnerable


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
    print(f"a: {a.name} at {a.position}, facing {a.facing_direction}")
    print(f"moving a to (3, 3)")
    a.move_to(3, 3)
    print(f"moving down")
    a.move_down()
    print(f"a: {a.name} at {a.position}, facing {a.facing_direction}")
    print("moving left")
    a.move_left()
    print(f"a: {a.name} at {a.position}, facing {a.facing_direction}")
