import math
from collections import Counter
from dataclasses import dataclass, field
from functools import singledispatchmethod, wraps
from typing import Any, Literal, Tuple, Union

from ..armor import ClothArmor
from ..debuffs import MagicVulnerability

from .equipment import Gear, GearSet
from .equipment import Equipment
from .effects import Effect, Effects

from ..utilities.location import Point, bresenham, clean_name, distance_between, behinds


@dataclass
class _Character:
    position: Point


##############################
# ~~~ Ability Decorators ~~~ #
##############################

def _check_can_move(func):
    @wraps(func)
    def wrapper(self: 'Pawn', *args, **kwargs):
        
        if not self.rooted and not self.stunned:
            return func(self, *args, **kwargs)

        reason = ''
        if self.effects.rooted:
            reason = f"{self.name} is rooted!"
        if self.effects.stunned:
            reason = f"{self.name} is stunned!"
        self.action_history.append(
            Action(
                turn=self._turn,
                type='move',
                action_name=func.__name__,
                actor=self,
                target=kwargs.get('target', args[0]),
                failed=True,
                failed_reason=reason
            )
        )

    return wrapper


def _action_decorator(_func=None, *, cooldown: int = 1, melee: bool = False, affected_by_blind: bool = True, affected_by_root: bool = False):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(self: 'Pawn', *args, **kwargs):
            target: Pawn = kwargs.get('target', args[0] if args else self)

            reason = ''
            if self._is_dead:
                reason = f"{self.name} is dead!"
            elif self.effects.stunned:
                reason = f"{self.name} is stunned!"
            elif self.acted_this_turn:
                reason = f"{self.name} has already acted this turn!"
            elif self._ability_cooldowns.get(clean_name(func.__name__), 0) > 0:
                reason = f"{clean_name(func.__name__)} is on cooldown!"
            elif affected_by_root and self.effects.rooted:
                reason = f"{self.name} is rooted!"
            elif affected_by_blind and self.effects.blinded:
                reason = f"{self.name} is blinded!"
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

            if self._ability_cooldowns.get(clean_name(func.__name__), 0) == 0:
                self._ability_cooldowns[clean_name(func.__name__)] = cooldown
            self.acted_this_turn = True

            self.current_action = Action(
                turn=self._turn,
                type='ability',
                action_name=func.__name__,
                actor=self,
                target=target
            )
            self.action_history.append(self.current_action)
            if target != self:
                self.face(target.position)
            return func(self, *args, **kwargs)

        return wrapper

    if _func is None:
        return actual_decorator
    return actual_decorator(_func)


class Pawn(_Character):

    def __init__(self,
                 name,
                 position: Union[Point, Tuple[int, int]],
                 health_max: int,
                 symbol: str = '@',
                 gear: GearSet = ClothArmor()) -> None:

        self.name = name

        # position
        self._position = position if isinstance(
            position, Point) else Point(*position)
        self.facing_direction = Point(0, 0)

        # status
        self.health_max = health_max
        self._health = health_max
        self._is_dead: bool = False
        self._is_already_dead: bool = False
        self._was_hit: bool = False
        self.current_action: Union[Action, None] = None
        self._ability_cooldowns = {}

        # effects
        self.equipment = Equipment()
        self.equipment.equip(gear)
        self.effects = Effects()

        # internal use
        self.move_history = [self.position]
        self.action_history: list[Action] = []
        self._symbol = symbol
        self._turn = 0
        self.acted_this_turn = False
        self.moved_this_turn = False
        self.reports: dict[str, Any] = {}

    ####################
    # ~~~ Location ~~~ #
    ####################
    @property
    def position(self) -> Point:
        return self._position

    @position.setter
    def position(self, value: Union[Point, Tuple[int, int]]) -> None:
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
    def points_behind(self) -> Tuple[Point, ...]:
        return behinds(self.position, self.facing_direction)

    @property
    def positions_behind(self) -> Tuple[Point, ...]:
        return self.points_behind

    @property
    def symbol(self) -> str:
        if self.is_alive:
            return self._symbol
        return "💀"

    ##################
    # ~~~ Status ~~~ #
    ##################

    @property
    def cooldowns(self) -> dict[str,int]:
        return {name : cooldown
                for name, cooldown in self._ability_cooldowns.items()
                if cooldown > 0}

    def is_on_cooldown(self, ability_name: str) -> bool:
        '''
        Checks the cooldowns for the name of an ability.
        Returns True if the ability is on cooldown.
        '''
        return self._ability_cooldowns.get(clean_name(ability_name), 0) > 0

    def get_cooldown(self, ability_name: str) -> int:
        '''
        Get the cooldown for an ability.
        Returns 0 if the ability is not on cooldown.
        '''
        return self._ability_cooldowns.get(clean_name(ability_name), 0)

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
    def health_percent(self) -> float:
        return round(self.health / self.health_max, 2)

    @property
    def is_alive(self) -> bool:
        return not self._is_dead

    @property
    def last_action_failed(self) -> bool:
        return bool(self.action_history) and self.action_history[-1].failed

    ########################
    # ~~~ Measurements ~~~ #
    ########################

    def distance_to(self, other: Union['Pawn', _Character, Point, tuple]) -> float:
        '''
        Get the distance between this character and another character or a board square.
        '''
        if hasattr(other, 'position'):
            return distance_between(self.position, other.position) # type: ignore
        elif isinstance(other, Point):
            return distance_between(self.position, other)
        elif isinstance(other, tuple):
            return distance_between(self.position, Point(*other))
        raise TypeError(f"Cannot calculate distance to {other} of type {type(other)}")

    def distance_from(self, other: Union['Pawn', _Character, Point, tuple]) -> float:
        return self.distance_to(other) # type: ignore

    def is_behind(self, other: 'Pawn') -> bool:
        return other.position in self.points_behind

    ####################
    # ~~~ Movement ~~~ #
    ####################
    def move(self, destination: Point) -> None:
        if not self._is_dead:
            return self.move_toward(destination)

    @_check_can_move
    def move_toward(self, target: Union[Point, _Character, tuple]) -> None:
        """
        Move one square in a straight line toward the provided Pawn or Point (x,y) tuple,
        as calculated using Bresenham's algorithm. Does not take into account impassible
        or dangerous terrain -- that is, using this movement method, the pawn might
        attempt to move into a wall and fail the move. Example:
        `hero.move_toward( boss )` or `hero.move_toward( Point(5, 5) )`"""
        if not self._is_dead:
            if isinstance(target, _Character):
                target = target.position
            elif isinstance(target, tuple):
                target = Point(*target)

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

    @singledispatchmethod
    def _teleport(self, x: int, y: int) -> None:
        self.move_history.append(Point(x, y))
        if self.distance_from((x, y)) > 1.5:
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

    @_check_can_move
    def move_up(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x, self.position.y+1)
            self.face(self.position.x, self.position.y+1)

    @_check_can_move
    def move_left(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x-1, self.position.y)
            self.face(self.position.x-1, self.position.y)

    @_check_can_move
    def move_right(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x+1, self.position.y)
            self.face(self.position.x+1, self.position.y)

    @_check_can_move
    def move_down(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x, self.position.y-1)
            self.face(self.position.x, self.position.y-1)

    @_check_can_move
    def move_down_right(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x+1, self.position.y-1)
            self.face(self.position.x+1, self.position.y-1)

    @_check_can_move
    def move_up_right(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x+1, self.position.y+1)
            self.face(self.position.x+1, self.position.y+1)

    @_check_can_move
    def move_down_left(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x-1, self.position.y-1)
            self.face(self.position.x-1, self.position.y-1)

    @_check_can_move
    def move_up_left(self) -> None:
        if not self._is_dead:
            self.position = Point(self.position.x-1, self.position.y+1)
            self.face(self.position.x-1, self.position.y+1)

    ##################
    # ~~~ Combat ~~~ #
    ##################

    @property
    def _base_damage(self) -> int:
        return self.equipment.bonus_damage_output + int(round(self.equipment.bonus_damage_output * self.equipment.bonus_damage_output_percent)) + sum([e.deal_bonus_damage_amount for e in self.effects.deal_damage_effects])

    @property
    def _damage_multiplier(self) -> float:
        return sum([e.deal_bonus_damage_percent for e in self.effects.deal_damage_effects])

    def calculate_damage(self, damage, target) -> int:
        dmg = damage + self._base_damage
        for effect in self.effects.deal_damage_effects:
            effect.on_activate(user=self, total_damage=dmg, target=target)
        return dmg + math.ceil(dmg * self._damage_multiplier)

    def _tick_damage(self, effect: Effect) -> None:
        if effect.damage_over_time > 0:
            self.health -= effect.damage_over_time
            self.action_history.append(Action(
                turn=self._turn,
                type='damage',
                action_name=f'{effect.name} ticked for {effect.damage_over_time} damage',
                actor=effect.name,
                target=self,
                target_effects=self.effects.to_dict(),
                ability_used=effect.name,
                damage=effect.damage_over_time,
            ))
        
        if effect.heal_over_time:
            self._heal(effect.heal_over_time)
            self.action_history.append(Action(
                turn=self._turn,
                type='damage',
                action_name=f'{effect.name} healed for {effect.heal_over_time} health',
                actor=effect.name,
                target=self,
                target_effects=self.effects.to_dict(),
                ability_used=effect.name,
                damage=effect.heal_over_time,
            ))
        
        if self.health <= 0:
            if not self._is_already_dead:
                    self._is_already_dead = True
                    self.reports['death'] = f'{self.name} died on turn {self._turn}!'
            self.health = 0
            self._is_dead = True

    def _take_damage(self, damager: 'Pawn', damage: int, damage_type: str, ability=False, ability_name="") -> None:
        barriers = self.effects.get_any_category_name('barrier') # cancels damage
        if barriers:
            barriers[0].on_activate(
                damager=damager,
                total_damage=damage,
                damage_type=damage_type
            )
            return

        parry = self.effects.get_any_category_name('parry') # cancels damage but needs to happen after barrier
        if parry:
            parry[0].on_activate(
                damager=damager,
                total_damage=damage,
                damage_type=damage_type
            )
            return
        
        for effect in self.effects.get_any_category_name('damage_activate'): # only things that don't change the damage but react to it
            effect.on_activate(
                damager=damager,
                total_damage=damage,
                damage_type=damage_type
            )

        if damager is not None:
            # trigger reflect
            self.effects._trigger_reflect(self, damager, damage)

        # damage mitigation due to armor
        damage -= int(round(self.equipment.damage_reduction_percent * damage))

        # trigger vulnerabilities
        if damage_type == "magic":
            increase = sum(
                [effect.take_bonus_damage_percent for effect in self.effects.find_effect_text('magic vulnerability')])
            damage += int(round(increase * damage))
            self.effects.remove_name('magic vulnerability')

        elif damage_type == "poison":
            if self.effects.find_effect_text('poison vulnerability'):
                damage *= 2

        dam_reduce = sum([effect.take_bonus_damage_percent for effect in self.effects.get_any_category_name('modifier')]) # buff/debuffs that affect damage taken on self
        damage += round(dam_reduce*damage)
        for effect in self.effects.get_any_category_name('modifier'):
            effect.on_activate(
                damager=damager,
                total_damage=damage,
                damage_type=damage_type
            )

        # trigger resistances
        resists = sum([effect.take_bonus_damage_percent for effect in self.effects.find_effect_text(f'{damage_type} resist')])
        damage -= int(round(resists * damage))

        # update action log with damage taken
        self.action_history.append(
            Action(
                turn=self._turn,
                type="damage",
                action_name=f"{self.name} took {damage if damage >= 0 else 0} damage from {damager.name if isinstance(damager, Pawn) else 'the tile'}!",
                actor=damager,
                target=self,
                failed=False,
                damage=damage,
                ability_used=ability_name if ability else (damager.current_action.action_name if isinstance(damager, Pawn) else 'Tile'), #type: ignore
                actor_effects=damager.effects.to_dict() if isinstance(damager, Pawn) else None,
                target_effects=self.effects.to_dict()
            ))

        if damage > 0:
            self.health -= damage
            self._was_hit = True

            if self.health <= 0:
                if not self._is_already_dead:
                    self._is_already_dead = True
                    self.reports['death'] = f'{self.name} died on turn {self._turn}!'
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

    def damage_report(self) -> list[dict[str, Any]]:
        dr = []
        for action in self.action_history:
            if action.damage is not None:
                dr.append(
                    {'turn':action.turn,
                    'damage':action.damage,
                    'ability':action.ability_used,
                    'source':action.actor,
                    'damager_effects':action.actor_effects,
                    'target_effects':action.target_effects}
                )
        return dr

    ###############################
    # ~~~ Passthrough Methods ~~~ #
    ###############################

    def has_effect(self, effect: Union[str, Effect]) -> bool:
        return self.effects.count(effect) > 0

    def equip(self, item: Union[Gear, GearSet]) -> None:
        return self.equipment.equip(item)

    def unequip(self, item: Union[Gear, GearSet, str]) -> None:
        return self.equipment.unequip(item)

    @property
    def poisoned(self) -> bool:
        return self.effects.poisoned

    @property
    def rooted(self) -> bool:
        return self.effects.rooted

    @property
    def stunned(self) -> bool:
        return self.effects.stunned

    @property
    def blinded(self) -> bool:
        return self.effects.blinded

    @property
    def active_effects(self) -> list[str]:
        return [e.name for e in self.effects.active_effects]

    @property
    def vulnerable(self) -> bool:
        return self.effects.vulnerable

    @property
    def vulnerabilities(self) -> list[Effect]:
        return self.effects.vulnerabilities

    def vulnerable_to(self, damage_type: str):
        """
        Returns True if the pawn is vulnerable to the given damage type.

        e.g. 
        `pawn.vulnerable_to('magic')` -> `True`
        """
        return self.effects.vulnerable_to(damage_type)

    @property
    def resistances(self) -> list[Effect]:
        return self.effects.resistances

    def resistant_to(self, damage_type: str):
        """
        Returns True if the pawn is resistant to the given damage type.

        e.g. 
        `pawn.resistant_to('magic')` -> `True`
        """
        return self.effects.resistant_to(damage_type)

    #############################
    # ~~~ Effect Management ~~~ #
    #############################

    # TODO: THIS IS A DUPE I THINK
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

        # TODO: magic vulnerability from fire + frost vuln pair
        frost = self.effects.find_effect_text('frost resistance')
        fire = self.effects.find_effect_text('fire resistance')
        if frost and fire:
            for ice_effect, fire_effect in zip(frost, fire):
                self.effects.add(MagicVulnerability())
                self.effects.remove_one(ice_effect)
                self.effects.remove_one(fire_effect)

        # increment turn counter
        self._turn += 1

    def _post_tick(self) -> None:
        # tick self.effects
        self.effects._tick()  # updates durations and removes expired effects

        # decrement ability cooldowns
        if self._ability_cooldowns:
            for name, cooldown in self._ability_cooldowns.items():
                if cooldown > 0:
                    self._ability_cooldowns[name] -= 1

        # reset action flags
        self.acted_this_turn = False
        self.moved_this_turn = False
        self._was_hit = False
        self.current_action = None

    def stacks(self, effect: Union[str, Effect]) -> int:
        '''
        Return the number of stacks of the specified effect that are currently active on the player.

        e.g. stacks('poison') -> 2
        or   stacks(Poison()) -> 2
        '''
        return self.effects.count(effect)

    @property
    def _marquis(self) -> str:
        # | ❤️❤️❤️❤️❤️❤️🖤🖤🖤 | 🦶 | Oingo Boingo     | 💚2, 💪4, 👀

        health = '❤️' * math.ceil((self.health / self.health_max) * 10)

        empty_health = '🖤' * (10 - len(health)//2)
        action = '🦶' if self.moved_this_turn else '👊'

        return f"| {health}{empty_health} | {action} | {self.symbol}:{self.name:<20} | {self.effects._marquis:<40}"

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
    actor: Union[Pawn, str]
    target: Union[Pawn, Point, str, None]
    failed: bool = field(default=False, init=True)
    failed_reason: str = field(default='', init=True)
    ability_used: Union[str, None] = field(default=None, init=True)
    damage: Union[int, None] = field(default=None, init=True)
    actor_effects: Union[Counter, None] = field(default=None, init=True)
    target_effects: Union[Counter, None] = field(default=None, init=True)

    def __post_init__(self):
        self.action_name = clean_name(self.action_name)
        if isinstance(self.actor, Pawn):
            self.actor = f"{self.actor.name} the {clean_name(self.actor.__class__.__name__)}"
        if isinstance(self.target, Pawn):
            self.target = f"{self.target.name} the {clean_name(self.target.__class__.__name__)}"

    def __repr__(self):
        if self.type == "damage":
            return self.action_name

        message = f"Turn {self.turn}: {self.actor} "

        # if it's an ability or a move
        if self.type == 'ability':
            message += "tried to use " if self.failed else "used "
        elif self.type == 'move':
            message += "tried to move " if self.failed else 'moved '
        elif self.type == 'damage':
            message += "tried to damage " if self.failed else "damaged "

        # if it didn't fail and it's an ability with a target
        if (self.type == 'ability' and self.target is not None):
            message += f"{self.action_name} on {self.target}"
        elif self.type == 'damage':
            message += f"{self.target.name if hasattr(self.target, 'name') else self.target}!" # type: ignore
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

if __name__ == "__main__":
    p = Pawn(name="Oingo Boingo", position=(0,0), health_max=100)
    print(f"Pawn named {p.name} at position {p.position} with {p.health}/{p.health_max} HP")
    print(p)
