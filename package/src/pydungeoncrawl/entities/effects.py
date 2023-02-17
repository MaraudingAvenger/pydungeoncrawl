import time
import hashlib
from collections import Counter
from typing import Iterator, Union

_SORT_PRIORITY = {
    "Might": 1,
    "Toughness": 2,
    "Frailty": 3,
    "Expose Weakness": 4,
    "Barrier": 5,
    "HoT": 6,
    "DoT": 7,
    "Blind": 8,
    "Stun": 9,
    "Root": 10,
    "Reflect": 11
}


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

    def __init__(self,
                 name: str,
                 category: set[str] | None = None,
                 duration: Union[int, float] = float("inf"),
                 description: str = "",
                 new: bool = True,
                 symbol: str = "⚙",
                 _stamp: float = time.time(),
                 bonus_movement: int = 0,
                 heal_over_time: int = 0,
                 bonus_max_health: int = 0,
                 bonus_max_health_percent: float = 0,
                 damage_over_time: int = 0,
                 deal_bonus_damage_amount: int = 0,
                 deal_bonus_damage_percent: float = 0,
                 take_bonus_damage_amount: int = 0,
                 take_bonus_damage_percent: float = 0,
                 reflect_damage_amount: int = 0,
                 reflect_damage_percent: float = 0):

        self.name = name
        self.duration = duration
        self.category = category or set()
        self.description = description
        self.new = new
        self.symbol = symbol
        self._stamp = _stamp
        self.bonus_movement: int = bonus_movement
        self.heal_over_time: int = heal_over_time
        self.bonus_max_health: int = bonus_max_health
        self.bonus_max_health_percent: float = bonus_max_health_percent
        self.damage_over_time: int = damage_over_time
        self.deal_bonus_damage_amount: int = deal_bonus_damage_amount
        self.deal_bonus_damage_percent: float = deal_bonus_damage_percent
        self.take_bonus_damage_amount: int = take_bonus_damage_amount
        self.take_bonus_damage_percent: float = take_bonus_damage_percent
        self.reflect_damage_amount: int = reflect_damage_amount
        self.reflect_damage_percent: float = reflect_damage_percent

    def on_create(self, *args, **kwargs):
        ...
    
    def on_expire(self, *args, **kwargs):
        ...
    
    def on_tick(self, *args, **kwargs):
        ...

    def on_activate(self, *args, **kwargs):
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.duration} turn{'s' if self.duration != 1 else ''})"

    def __str__(self):
        return self.symbol

    def __eq__(self, other):
        if not isinstance(other, Effect):
            raise NotImplemented("Cannot compare Effect to non-Effect object")
        return self.__hash__() == other.__hash__() 

    def __hash__(self) -> int:
        return int.from_bytes(hashlib.md5(''.join((
            self.name, ''.join(self.category), self.description, self.symbol
        )).encode()).digest(), byteorder='big')


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
        for effect in self.get_any_category_name('reflect'):
            target._take_damage(
                damager,
                int(round(damage * effect.reflect_damage_percent +
                    effect.reflect_damage_amount)),
                damage_type='reflect',
                ability=True,
                ability_name="Reflect")

    ########################################
    # ~~ Add, remove, and count effects ~~ #
    ########################################

    def add(self, effect: Effect) -> None:
        'add a single effect to the collection'
        self._effects.append(effect)

    def add_stacks(self, effect_constructor, stacks=1, **kwargs) -> None:
        'add a number of stacks of an effect to the collection'
        for _ in range(stacks):
            self.add(effect_constructor(**kwargs))

    def remove(self, effect: Effect) -> None:
        'remove an effect from the collection'
        self._effects = list(
            filter(lambda e: e != effect, self._effects))

    def remove_category(self, category: str) -> None:
        'remove all effects in the collection with the given category'
        self._effects = list(
            filter(lambda e: category not in e.category, self._effects))

    def remove_name(self, name: str) -> None:
        'remove all effects in the collection with the given name'
        self._effects = list(
            filter(lambda e: e.name.lower() != name.lower(), self._effects))

    def remove_all(self, *effects: Effect) -> None:
        'remove one effect from the collection'
        for effect in effects:
            self.remove(effect)

    # TODO: __TEST THIS__
    def remove_one(self, effect: Effect) -> None:
        'remove one effect from the collection'
        self._effects.pop(self._effects.index(effect))

    def count(self, effect: Union[str, Effect]) -> int:
        'return the number of effects in the collection'
        if isinstance(effect, Effect):
            return len(list(filter(lambda e: e.name == effect.name, self._effects)))
        return len(list(filter(lambda e: e.name.lower() == effect.lower(), self._effects)))

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
    def resistances(self) -> list[Effect]:
        'return a list of Resistance effects in the collection'
        return [effect for effect in self._effects if 'resist' in effect.name.lower()]

    def resistant_to(self, damage_type:str) -> bool:
        'return True if the collection contains a Resistance effect of the specified damage type'
        if (resists := self.resistances):
            return any(damage_type.lower() in e.name.lower() for e in resists)
        return False

    @property
    def vulnerable(self):
        return bool(self.vulnerabilities)

    @property
    def has_active_effects(self):
        return len(self._effects) > 0

    @property
    def active_effects(self) -> list[Effect]:
        return list(set(self._effects))

    #################
    # ~~ Getters ~~ #
    #################

    def get_all_category_name(self, *categories: str) -> list[Effect]:
        'return a list of effects in the collection that have all the specified categories'
        return list(filter(
            lambda e: all(category.lower()
                          in e.category for category in categories),
            self._effects))

    def get_any_category_name(self, *categories: str) -> list[Effect]:
        'return a list of effects in the collection that have the specified category'
        return list(filter(
            lambda e: any(category.lower()
                          in e.category for category in categories),
            self._effects))

    def get_category_effects(self, category: str, ) -> 'Effects':
        'return a new Effects collection of effects in the collection that have the specified category'
        return Effects(*self.get_any_category_name(category))

    def find_effect_text(self, text: str) -> list[Effect]:
        'return a list of effects in the collection that have the specified text'
        return list(filter(lambda e: text.lower() in e.name.lower(), self._effects))

    def find_effect_exact_text(self, text: str) -> Effect | None:
        'return an effect in the collection that has the specified text'
        return next(filter(lambda e: text.lower() == e.name.lower(), self._effects), None)

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
    def deal_damage_effects(self) -> list[Effect]:
        'return a list of effects in the collection that cause bearer to deal extra damage'
        return [e
                for e in self._effects
                if any(getattr(e, property) != 0
                       for property in [
                    'deal_bonus_damage_amount',
                    'deal_bonus_damage_percent']
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

    def get_damage_over_time_effects(self) -> list[Effect]:
        'return a new `Effects` object of effects in the collection that deal damage over time'
        return [effect for effect in self._effects if effect.damage_over_time != 0]

    def get_dot_effects(self) -> list[Effect]:
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

    @property
    def _marquis(self) -> str:
        return " ".join([f"{effect.symbol}{self.count(effect):<2}"
                         for effect in sorted(
                             self.active_effects,
                             key=lambda e: _SORT_PRIORITY.get(e.name, 100))
                         ])

    ########################
    # ~~ Dunder methods ~~ #
    ########################

    def to_dict(self):
        return Counter(e.name for e in self._effects)

    def __repr__(self) -> str:
        return f'Effects({self._effects})'

    def __str__(self) -> str:
        return f'Effects({self._effects})'

    def __iter__(self) -> Iterator[Effect]:
        return iter(self._effects)

    def __getitem__(self, index: int) -> Effect:
        return self._effects[index]

    def __len__(self) -> int:
        return len(self._effects)
