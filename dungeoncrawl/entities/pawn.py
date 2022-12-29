from dataclasses import dataclass, field
from functools import singledispatchmethod, wraps
from typing import Literal

from dungeoncrawl.entities.equipment import Gear, GearSet
from dungeoncrawl.entities.equipment import Equipment
from dungeoncrawl.entities.effects import Effect, Effects
from dungeoncrawl.utilities.location import Point, bresenham, clean_name, distance_between, behinds


@dataclass
class _Character:
    position: Point


class Pawn(_Character):

    def __init__(self,
                 name,
                 position: Point | tuple[int, int],
                 health_max: int,
                 symbol: str = '@') -> None:

        self.name = name

        # position
        self._position = position if isinstance(
            position, Point) else Point(*position)
        self.facing_direction = Point(0, 0)

        # status
        self.health_max = health_max
        self._health = health_max
        self._is_dead: bool = False
        self._was_hit: bool = False
        self.current_action: Action | None = None
        self.ability_cooldowns = {}

        # effects
        self.equipment = Equipment()
        self.effects = Effects()

        # internal use
        self.move_history = [self.position]
        self.action_history: list[Action] = []
        self._symbol = symbol
        self._turn = 0
        self.acted_this_turn = False
        self.moved_this_turn = False

    ####################
    # ~~~ Location ~~~ #
    ####################
    @property
    def position(self) -> Point:
        return self._position

    @position.setter
    def position(self, value: Point | tuple[int, int]) -> None:
        if not self.moved_this_turn:
            self._position = value if isinstance(
                value, Point) else Point(*value)
            self.acted_this_turn = True
            self.moved_this_turn = True
            self.move_history.append(self.position)
            self.action_history.append(
                Action(
                    turn=self._turn,
                    type='move',
                    action_name='move',
                    actor=self,
                    target=self.position
                )
            )

    def _revert_position(self, message: str) -> None:
        bad_position = self.position
        self.move_history = self.move_history[:-1]
        self._position = self.move_history[-1]
        self.action_history.append(
            Action(
                turn=self._turn,
                type="move",
                action_name="move",
                actor=self,
                target=bad_position,
                failed=True,
                failed_reason=message
            )
        )

    @property
    def points_behind(self) -> tuple[Point, ...]:
        return behinds(self.position, self.facing_direction)

    @property
    def symbol(self) -> str:
        if self.is_alive:
            return self._symbol
        return "💀"

    ##################
    # ~~~ Status ~~~ #
    ##################

    @property
    def cooldowns(self) -> list[str]:
        return [name for name, cooldown in self.ability_cooldowns.items() if cooldown > 0]

    def is_on_cooldown(self, ability_name: str) -> bool:
        return self.ability_cooldowns.get(ability_name, 0) > 0

    def cooldown(self, ability_name: str) -> int:
        return self.ability_cooldowns.get(ability_name, 0)

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

    @property
    def is_alive(self) -> bool:
        return not self._is_dead

    @property
    def last_action_failed(self) -> bool:
        return bool(self.action_history) and self.action_history[-1].failed

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

    ####################
    # ~~~ Movement ~~~ #
    ####################
    def move(self, destination: Point) -> None:
        if not self._is_dead:
            return self.move_toward(destination)

    @singledispatchmethod
    def _teleport(self, x: int, y: int) -> None:
        if self.distance_from(x, y) > 1.5:
            self.position = Point(x, y)
            return
        self.facing_direction = Point(
            x+(x-self.position.x), y+(y-self.position.y))
        self.position = Point(x, y)

    @_teleport.register
    def _(self, point: Point) -> None:
        self._teleport(point.x, point.y)

    @singledispatchmethod
    def face(self, target: _Character) -> None:
        self.facing_direction = next(bresenham(self.position, target.position))

    @face.register
    def _(self, target: Point) -> None:
        self.facing_direction = next(bresenham(self.position, target))

    @face.register
    def _(self, x: int, y: int) -> None:
        self.facing_direction = next(bresenham(self.position, Point(x, y)))

    def move_up(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x, self.position.y+1)
            self.face(self.position.x, self.position.y+1)

    def move_left(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x-1, self.position.y)
            self.face(self.position.x-1, self.position.y)

    def move_right(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x+1, self.position.y)
            self.face(self.position.x+1, self.position.y)

    def move_down(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x, self.position.y-1)
            self.face(self.position.x, self.position.y-1)

    def move_down_right(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x+1, self.position.y-1)
            self.face(self.position.x+1, self.position.y-1)

    def move_up_right(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x+1, self.position.y+1)
            self.face(self.position.x+1, self.position.y+1)

    def move_down_left(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x-1, self.position.y-1)
            self.face(self.position.x-1, self.position.y-1)

    def move_up_left(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x-1, self.position.y+1)
            self.face(self.position.x-1, self.position.y+1)

    @singledispatchmethod
    def move_toward(self, target: Point|_Character) -> None:
        if not self._is_dead:
            if isinstance(target, _Character):
                target = target.position

            if self.distance_from(target) > 1.5:
                path = bresenham(self.position, target)
                self.position = next(path)
                self.face(next(path))
            else:
                add = (target.x-self.position.x, target.y-self.position.y)
                self.position = target
                self.face(Point(
                    target.x+(add[0]),
                    target.y+(add[1])
                ))

    @move_toward.register
    def _(self, x: int, y: int) -> None:
        self.move_toward(Point(x, y))

    
    ##################
    # ~~~ Combat ~~~ #
    ##################

    def _tick_damage(self, effect: Effect) -> None:
        self.health -= effect.damage_over_time
        self.health += effect.heal_over_time

        if self.health <= 0:
            self.health = 0
            self._is_dead = True
    

    def _take_damage(self, damager: 'Pawn', damage: int, damage_type: str) -> None:
        #print(self.__class__.__name__, 'took damage!')

        if damager is not None:
            # trigger reflect
            self.effects._trigger_reflect(self, damager, damage)

        # damage mitigation due to armor
        damage -= int(round(self.equipment.damage_reduction_percent * damage))

        # trigger vulnerabilities
        if damage_type == "magic":
            reduction = sum([effect.take_bonus_damage_percent for effect in self.effects.find_effect_text(f'magic vuln')])
            damage += int(round(reduction * damage))
            self.effects.remove_all(f'magic vulnerabilty')

        elif damage_type == "poison":
            if self.effects.find_effect_text(f'poison vulnerability'):
                damage *= 2


        for effect in self.effects.get_extra_damage_effects():
            number_damage = effect.take_bonus_damage_amount
            percent_damage = int(round(effect.take_bonus_damage_percent * damage))
            
            # trigger the effect on_activate method just in case it has one
            effect.on_activate(
                damager = damager,
                total_damage = damage,
                calculated_damage = number_damage + percent_damage)

            damage += (number_damage + percent_damage)

            if damage == 0:
                break
        # trigger resistances        
        reduction = sum([effect.take_bonus_damage_percent for effect in self.effects.find_effect_text(f'{damage_type} resist')])
        damage -= int(round(reduction * damage))

        # update action log with damage taken
        self.action_history.append(
            Action(self._turn, "damage", f"{self.name} took {damage if damage >= 0 else 0} damage from {damager.name}!", damager, self, failed=False))

        if damage > 0:
            self.health -= damage
            self._was_hit = True

            if self.health <= 0:
                self.health = 0
                self._is_dead = True

    def _heal(self, amount: int, force=False) -> None:
        if not self._is_dead or force:
            self.health += amount
            if self.health > self.health_max:
                self.health = self.health_max

            # alive them if they have health
            if force and self.health > 0:
                self._is_dead = False


    ###############################
    # ~~~ Convenience Methods ~~~ #
    ###############################

    def equip(self, item: Gear | GearSet) -> None:
        return self.equipment.equip(item)

    def unequip(self, item: Gear | GearSet | str) -> None:
        return self.equipment.unequip(item)

    @property
    def poisoned(self):
        return self.effects.poisoned

    @property
    def rooted(self):
        return self.effects.rooted

    @property
    def stunned(self):
        return self.effects.stunned

    @property
    def blinded(self):
        return self.effects.blinded

    @property
    def active_effects(self):
        return self.effects.active

    @property
    def vulnerable(self):
        return self.effects.vulnerable

    @property
    def vulnerabilities(self):
        return self.effects.vulnerabilities

    def vulnerable_to(self, damage_type: str):
        return self.effects.vulnerable_to(damage_type)

    #############################
    # ~~~ Effect Management ~~~ #
    #############################

    def _add_effect(self, effect: Effect) -> None:
        self.effects.add(effect)

    def _tick(self) -> None:
        # apply effects
        for effect in self.effects:
            if effect.new:
                effect.on_create()
                effect.new = False
            effect.on_tick()
            self._tick_damage(effect)

        # tick self.effects
        self.effects._tick()  # updates durations and removes expired effects

        # decrement ability cooldowns
        if self.ability_cooldowns:
            for name, cooldown in self.ability_cooldowns.items():
                if cooldown > 0:
                    self.ability_cooldowns[name] -= 1

        # reset action flags
        self.acted_this_turn = False
        self.moved_this_turn = False
        self._was_hit = False
        self.current_action = None

        # increment turn counter
        self._turn += 1

    @singledispatchmethod
    def stacks(self, effect: Effect) -> int:
        'return the number of stacks of the specified effect in the collection'
        return self.effects.count(effect)

    @stacks.register
    def _(self, effect_name: str) -> int:
        'return the number of stacks of the specified effect in the collection'
        return self.effects.count(effect_name)

    ##########################
    # ~~~ Dunder Methods ~~~ #
    ##########################

    def __repr__(self) -> str:
        return f"{self.name} ({clean_name(self.__class__.__name__)}), {self.health}/{self.health_max} HP"

    def __str__(self) -> str:
        return f"{self.name} ({clean_name(self.__class__.__name__)}), {self.health}/{self.health_max} HP"


@dataclass
class Action:
    turn: int
    type: Literal['ability', 'move', 'damage']
    action_name: str
    actor: Pawn | str
    target: Pawn | None | Point | str
    failed: bool = field(default=False, init=True)
    failed_reason: str = field(default='', init=True)

    def __post_init__(self):
        self.action_name = clean_name(self.action_name)
        if isinstance(self.actor, Pawn):
            self.actor = f"{self.actor.name} the {clean_name(self.actor.__class__.__name__)}"
        if isinstance(self.target, Pawn):
            self.target = f"{self.target.name} the {clean_name(self.target.__class__.__name__)}"

    def __repr__(self):
        message = f"Turn {self.turn}: {self.actor} "

        # if it's an ability or a move
        if self.type == 'ability':
            message += "tried to use " if self.failed else "used "
        elif self.type == 'move':
            message += "tried to move " if self.failed else 'moved '

        # if it didn't fail and it's an ability with a target
        if (self.type == 'ability' and self.target is not None):
            message += f"{self.action_name} on {self.target}"

        # if it didn't fail and it's a move
        elif isinstance(self.target, Point) and self.type == 'move':
            message += f"to {self.target}"

        # if it didn't fail and it's an ability without a target
        else:
            message += f"{self.action_name}"

        # if it failed (continued)
        if self.failed and self.failed_reason:
            message += f", but failed because {self.failed_reason}"
        elif self.failed:
            message += ", but failed!"

        return message

    def __str__(self):
        return self.__repr__()


def _action_decorator(_func=None, *, cooldown: int = 1, melee: bool = False):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            target: Pawn = kwargs.get('target', args[0])

            reason = ''
            if self._is_dead:
                reason = f"{self.name} is dead!"
            elif self.acted_this_turn:
                reason = f"{self.name} has already acted this turn!"
            elif self.ability_cooldowns.get(clean_name(func.__name__), 0) > 0:
                reason = f"{clean_name(func.__name__)} is on cooldown!"
            elif melee and distance_between(self.position, target.position) > 1.5:
                reason = f"{target.name} was too far away"

            if reason:
                self.action_history.append(
                    Action(
                        turn=self._turn,
                        type='ability',
                        action_name=func.__name__,
                        actor=self,
                        target=target,
                        failed=True,
                        failed_reason=reason
                    )
                )
                return

            if self.ability_cooldowns.get(clean_name(func.__name__), 0) == 0:
                self.ability_cooldowns[clean_name(func.__name__)] = cooldown
            self.acted_this_turn = True

            self.current_action = Action(
                turn=self._turn,
                type='ability',
                action_name=func.__name__,
                actor=self,
                target=target
            )
            self.action_history.append(self.current_action)

            return func(self, *args, **kwargs)

        return wrapper

    if _func is None:
        return actual_decorator
    return actual_decorator(_func)


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
    a._teleport(Point(2, 2))
    print(f"a: {a.name} at {a.position}, facing {a.facing_direction}")
    print(f"moving a to (3, 3)")
    a._teleport(3, 3)
    print(f"moving down")
    a.move_down()
    print(f"a: {a.name} at {a.position}, facing {a.facing_direction}")
    print("moving left")
    a.move_left()
    print(f"a: {a.name} at {a.position}, facing {a.facing_direction}")
