from dataclasses import dataclass, field
from functools import singledispatchmethod
from typing import Iterator

@dataclass
class Effect:
    """
    A class that represents an effect.  

    `name` [str] is the name of the effect.  

    `duration` [int|float("inf")] This indicates the number of ticks that the effect will remain active.
    The default duration is infinite (`float("inf")`).  

    `damage_over_time` [int] This is the amount of damage that the bearer of the effect will take each
    tick. The default value is zero. Negative values will heal the bearer of the effect.

    `bonus_damage` [int] This affects the amount of damage that the bearer of the effect deals. Positive
    values increase damage, negative values decrease damage.

    `bonus_damage_received` [int] This affects the amount of damage that the bearer of the effect will
    receive. Positive values increase the damage that the bearer receives, negative values decrease it.  

    `bonus_movement` [int] is an integer amount of bonus grid squares that the pawn will be able to move
    each tick. See the Haste effect for an example of this. Positive values will increase the number of
    squares that a Pawn can move, and negative values will decrease the number of squares. The default
    value is zero.  

    `bonus_max_health` [int] is the amount of hit points added to the Pawn's maximum hit points when this
    effect is applied. A positive number will increase the Pawn's maximum hit points; a negative number
    will decrease the Pawn's hit points. The default value is zero.
    """
    name: str = field(init=True, repr=True, hash=True)
    duration: int | float = field(init=True, default=1, repr=True, hash=False)
    category: set[str] = field(init=True, default_factory=set, repr=True, hash=True)
    description: str = field(init=True, default="", repr=True, hash=False)
    new: bool = field(init=False, default=True, repr=False, hash=False)

    # ~~~ Callbacks ~~~#
    # TODO: implement all these in the Effects class
    on_create: callable = field( # type: ignore
        init=True, default=lambda *x, **y: None, hash=False, repr=False)
    on_expire: callable = field( # type: ignore
        init=True, default=lambda *x, **y: None, hash=False, repr=False)
    on_tick: callable = field( # type: ignore
        init=True, default=lambda *x, **y: None, hash=False, repr=False)
    on_activate: callable = field( # type: ignore
        init=True, default=lambda *x, **y: None, hash=False, repr=False)

    # ~~~ Bonus effects ~~~#
    # movement
    bonus_movement: int = field(init=True, default=0, hash=False, repr=False)

    # healing and max health buffing
    heal_over_time: int = field(init=True, default=0, hash=False, repr=False)
    bonus_max_health: int = field(init=True, default=0, hash=False, repr=False)
    bonus_max_health_percent: float = field(
        init=True, default=0, hash=False, repr=False)

    # damage on tick
    damage_over_time: int = field(init=True, default=0, hash=False, repr=False)

    # damage when attacking
    deal_bonus_damage_amount: int = field(
        init=True, default=0, hash=False, repr=False)
    deal_bonus_damage_percent: float = field(
        init=True, default=0, hash=False, repr=False)

    # damage when being attacked
    
    ## can be positive or negative
    take_bonus_damage_amount: int = field(
        init=True, default=0, hash=False, repr=False)
    take_bonus_damage_percent: float = field(
        init=True, default=0, hash=False, repr=False)

    # triggered on _trigger_reflect, not otherwise
    reflect_damage_amount: int = field(
        init=True, default=0, hash=False, repr=False)
    reflect_damage_percent: float = field(
        init=True, default=0, hash=False, repr=False)


class Effects:
    '''
    Convenience class for a collection of effects.

    `add()`, `remove()` add or remove effects from the collection.

    `tick()` decrements the duration of the effects in the collection.

    `bonus_damage`, `bonus_damage_received`, `bonus_movement`, and`bonus_max_health` are all the collected
    values of the effects in the collection.
    '''

    def __init__(self, *effects: Effect):
        self._effects: list[Effect] = list(effects) if effects else []
        self._reflected = False
    
    
    #################################
    # ~~ Tick and trigger methds ~~ #
    #################################

    def _tick(self) -> None:
        'decrement the duration of all effects in the collection'
        self.reflected = False
        for effect in self._effects:
            effect.duration -= 1
            if effect.duration <= 0:
                effect.on_expire()
        self._effects = list(filter(lambda e: e.duration > 0, self._effects))

    def _trigger_reflect(self, damager, target, damage: int) -> None:
        'trigger the effects in the collection that reflect damage'
        self.reflected = True
        for effect in self.get_category('reflect'):
            target._take_damage(
                damager,
                int(round(damage * effect.reflect_damage_percent + effect.reflect_damage_amount)))

    
    ########################################
    # ~~ Add, remove, and count effects ~~ #
    ########################################

    def add(self, effect: Effect, stacks=1) -> None:
        'add an effect to the collection'
        # TODO: make effects stack
        for _ in range(stacks):
            self._effects.append(effect)

    @singledispatchmethod
    def remove_all(self, effect: Effect) -> None:
        'remove an effect from the collection'
        self._effects = list(
            filter(lambda e: e.name != effect.name, self._effects))

    @remove_all.register
    def _(self, effect_name: str) -> None:
        'remove an effect from the collection'
        self._effects = list(
            filter(lambda e: e.name.lower() != effect_name.lower(), self._effects))

    # TODO: make this work
    def remove_one(self, effect: Effect) -> None:
        'remove one effect from the collection'
        pass

    @singledispatchmethod
    def count(self, effect: Effect) -> int:
        'return the number of effects in the collection'
        return len(list(filter(lambda e: e.name.lower() == effect.name.lower(), self._effects)))

    @count.register
    def _(self, effect_name: str) -> int:
        'return the number of effects in the collection'
        return len(list(filter(lambda e: e.name.lower() == effect_name.lower(), self._effects)))

    
    #############################################
    # ~~~ Convenience properties and methods ~~~#
    #############################################

    @property
    def stunned(self) -> bool:
        'return True if the collection contains a Stun effect'
        return self.count('Stun') > 0

    @property
    def blinded(self) -> bool:
        'return True if the collection contains a Blind effect'
        return self.count('Blind') > 0

    @property
    def rooted(self) -> bool:
        'return True if the collection contains a Root effect'
        return self.count('Root') > 0

    @property
    def poisoned(self) -> bool:
        'return True if the collection contains a Poison effect'
        return self.count('Poison') > 0

    @property
    def vulnerabilities(self) -> list[Effect]:
        'return a list of Vulnerability effects in the collection'
        return [effect for effect in self._effects if 'vulnerab' in effect.name.lower()]

    def vulnerable_to(self, damage_type: str) -> bool:
        'return True if the collection contains a Vulnerability effect of the specified damage type'
        if (vulns := self.vulnerabilities):
            return any(damage_type.lower() in e.name.lower() for e in vulns)
        return False

    @property
    def vulnerable(self):
        return bool(self.vulnerabilities)

    @property
    def active(self):
        return len(self._effects) > 0

    
    #################
    # ~~ Getters ~~ #
    #################

    def get_category(self, category: str) -> list[Effect]:
        'return a list of effects in the collection that have the specified category'
        return list(filter(lambda e: category.lower() in set(map(lambda s: s.lower(),e.category)), self._effects))

    def get_category_effects(self, category: str) -> 'Effects':
        'return a new Effects collection of effects in the collection that have the specified category'
        return Effects(*self.get_category(category))

    def find_effect_text(self, text: str) -> list[Effect]:
        'return a list of effects in the collection that have the specified text'
        return list(filter(lambda e: text.lower() in e.name.lower(), self._effects))

    
    #####################################################
    # ~~ Effect type-specific getters and properties ~~ #
    #####################################################

    def get_extra_damage_effects(self) -> list[Effect]:
        'return a list of effects in the collection that cause bearer to take extra damage'
        return [e
                for e in self._effects
                if any(getattr(e, property) != 0
                       for property in [
                        'take_bonus_damage_amount',
                        'take_bonus_damage_percent']
                        )]

    @property
    def damage_over_time(self, use=False) -> int:
        if use:
            for effect in [e for e in self._effects if e.damage_over_time != 0]:
                effect.on_activate()
        return sum(effect.damage_over_time for effect in self._effects)

    @property
    def dot(self) -> int:
        'alias for `damage_over_time`'
        return self.damage_over_time

    def get_damage_over_time_effects(self) -> 'Effects':
        'return a new `Effects` object of effects in the collection that deal damage over time'
        return Effects(*[effect for effect in self._effects if effect.damage_over_time != 0])

    def get_dot_effects(self) -> 'Effects':
        'alias for `get_damage_over_time_effects()`'
        return self.get_damage_over_time_effects()

    @property
    def heal_over_time(self, use=False) -> int:
        'total amount of health that will be healed per turn'
        if use:
            for effect in [e for e in self._effects if e.heal_over_time != 0]:
                effect.on_activate()
        return sum(effect.heal_over_time for effect in self._effects)

    @property
    def hot(self) -> int:
        'alias for `heal_over_time`'
        return self.heal_over_time

    def get_heal_over_time_effects(self) -> 'Effects':
        return Effects(*[effect for effect in self._effects if effect.heal_over_time != 0])

    def get_hot_dot_effects(self) -> list[Effect]:
        return [effect for effect in self._effects
                if effect.heal_over_time != 0 or effect.damage_over_time != 0]

    @property
    def bonus_damage_output(self) -> int:
        return sum(effect.deal_bonus_damage_amount for effect in self._effects)

    def get_damage_output_effects(self) -> list[Effect]:
        return [effect for effect in self._effects if effect.deal_bonus_damage_amount != 0]

    @property
    def bonus_movement(self) -> int:
        return sum(effect.bonus_movement for effect in self._effects)

    def get_movement_effects(self) -> list[Effect]:
        return [effect for effect in self._effects if effect.bonus_movement != 0]

    @property
    def bonus_damage_received(self) -> int:
        return sum(effect.take_bonus_damage_amount for effect in self._effects)

    def get_damage_received_effects(self) -> list[Effect]:
        return [effect for effect in self._effects if effect.take_bonus_damage_amount != 0]

    @property
    def bonus_damage_received_percent(self) -> float:
        return sum(effect.bonus_damage_received_percent for effect in self._effects if not effect)

    def get_damage_received_percent_effects(self) -> list[Effect]:
        return [effect for effect in self._effects if effect.take_bonus_damage_percent != 0]

    @property
    def bonus_max_health(self) -> int:
        return sum(effect.bonus_max_health for effect in self._effects)

    def get_max_health_effects(self) -> list[Effect]:
        return [effect for effect in self._effects if effect.bonus_max_health != 0]

    
    ########################
    # ~~ Dunder methods ~~ #
    ########################

    def __repr__(self) -> str:
        return f'Effects({self._effects})'

    def __str__(self) -> str:
        return f'Effects({self._effects})'

    def __iter__(self) -> Iterator[Effect]:
        return iter(self._effects)
