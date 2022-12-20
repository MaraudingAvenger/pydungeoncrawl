from dataclasses import dataclass, field
from functools import singledispatchmethod


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
    duration: int | float = field(init=True, default=1, hash=False)
    category: str = field(init=True, default="none", hash=True)

    #~~~ Callbacks ~~~#
    #TODO: implement all these in the Effects class
    on_activate: callable = field(default=lambda: None, hash=False) # type: ignore
    on_deactivate: callable = field(default=lambda: None, hash=False) # type: ignore
    on_tick: callable = field(default=lambda: None, hash=False) # type: ignore
    on_use: callable = field(default=lambda: None, hash=False) # type: ignore

    bonus_movement: int = field(default=0, hash=False)

    damage_over_time: int = field(default=0, hash=False)
    
    #TODO: turn these into percentage based only? 
    bonus_damage_output: int = field(default=0, hash=False)
    bonus_damage_output_percent: float = field(default=0, hash=False)
    
    bonus_damage_received: int = field(default=0, hash=False)
    bonus_damage_received_percent: float = field(default=0, hash=False)
    
    bonus_max_health: int = field(default=0, hash=False)
    bonus_max_health_percent: float = field(default=0, hash=False)


class Effects:
    '''
    Convenience class for a collection of effects.

    `add()`, `remove()` add or remove effects from the collection.

    `tick()` decrements the duration of the effects in the collection.

    `bonus_damage`, `bonus_damage_received`, `bonus_movement`, and`bonus_max_health` are all the collected
    values of the effects in the collection.
    '''

    def __init__(self, *effects: Effect):
        self._effects: list[Effect] = [*effects] if effects else []

    def add(self, effect: Effect) -> None:
        'add an effect to the collection'
        #TODO: make effects stack
        self._effects.append(effect)

    @singledispatchmethod
    def remove_all(self, effect: Effect) -> None:
        'remove an effect from the collection'
        self._effects = list(filter(lambda e: e.name != effect.name, self._effects))
    @remove_all.register
    def _(self, effect_name: str) -> None:
        'remove an effect from the collection'
        self._effects = list(filter(lambda e: e.name != effect_name, self._effects))

    #TODO: make this work
    def remove_one(self, effect:Effect) -> None:
        'remove one effect from the collection'
        pass

    def tick(self) -> None:
        'decrement the duration of all effects in the collection'
        for effect in self._effects:
            effect.duration -= 1
        self._effects = list(filter(lambda e: e.duration > 0, self._effects))

    @singledispatchmethod
    def count(self, effect:Effect) -> int:
        'return the number of effects in the collection'
        return len(list(filter(lambda e: e.name.lower() == effect.name.lower(), self._effects)))
    @count.register
    def _(self, effect_name:str) -> int:
        'return the number of effects in the collection'
        return len(list(filter(lambda e: e.name.lower() == effect_name.lower(), self._effects)))

    def stunned(self) -> bool:
        'return True if the collection contains a Stun effect'
        return self.count('Stun') > 0

    def blind(self) -> bool:
        'return True if the collection contains a Blind effect'
        return self.count('Blind') > 0

    def root(self) -> bool:
        'return True if the collection contains a Root effect'
        return self.count('Root') > 0

    @property
    def active(self):
        return len(self._effects) > 0

    def get_category(self, category:str) -> list[Effect]:
        'return a list of effects in the collection that have the specified category'
        return list(filter(lambda e: e.category.lower() == category.lower(), self._effects))
    def get_category_effects(self, category:str) -> 'Effects':
        'return a new Effects collection of effects in the collection that have the specified category'
        return Effects(*self.get_category(category))

    def find_effect_text(self, text:str) -> list[Effect]:
        'return a list of effects in the collection that have the specified text'
        return list(filter(lambda e: text.lower() in e.name.lower(), self._effects))

    @property
    def damage_over_time(self, use=False) -> int:
        if use:
            for effect in [e for e in self._effects if e.damage_over_time != 0]:
                effect.on_use()
        return sum(effect.damage_over_time for effect in self._effects)
    def dot(self, use=False) -> int:
        'alias for `damage_over_time`'
        return self.damage_over_time(use=use)
    
    def get_damage_over_time_effects(self) -> 'Effects':
        return Effects(*[effect for effect in self._effects if effect.damage_over_time != 0])
    def get_dot_effects(self) -> 'Effects':
        'alias for `get_damage_over_time_effects()`'
        return self.get_damage_over_time_effects()

    @property
    def bonus_damage_output(self, use=False) -> int:
        return sum(effect.bonus_damage_output for effect in self._effects)
    def get_damage_output_effects(self) -> list[Effect]:
        return [effect for effect in self._effects if effect.bonus_damage_output != 0]

    @property
    def bonus_movement(self) -> int:
        return sum(effect.bonus_movement for effect in self._effects)
    def get_movement_effects(self) -> list[Effect]:
        return [effect for effect in self._effects if effect.bonus_movement != 0]

    @property
    def bonus_damage_received(self) -> int:
        return sum(effect.bonus_damage_received for effect in self._effects)
    def get_damage_received_effects(self) -> list[Effect]:
        return [effect for effect in self._effects if effect.bonus_damage_received != 0]

    @property
    def bonus_max_health(self) -> int:
        return sum(effect.bonus_max_health for effect in self._effects)
    def get_max_health_effects(self) -> list[Effect]:
        return [effect for effect in self._effects if effect.bonus_max_health != 0]


# some examples of effects that can be applied to Pawns
# spells
Burning = Effect(name="Burning", duration=3,  damage_over_time=2,
                 bonus_damage_received=0, bonus_movement=0)
Freezing = Effect(name="Freezing",  bonus_damage_output=1, duration=3,
                  bonus_damage_received=0, bonus_movement=-1)

Haste = Effect(name="Haste", duration=3,  bonus_damage_output=0,
               bonus_damage_received=0, bonus_movement=1)
Bless = Effect(name="Bless",  bonus_damage_output=0, duration=3,
               bonus_damage_received=-1, bonus_movement=0)

# Equipment effects
Frailty = Effect(name="Frailty", duration=float('inf'),
                bonus_damage_output=-1, bonus_damage_received=1, bonus_movement=0)
Fire = Effect(name="Fire",  bonus_damage_output=2, duration=0,
              bonus_damage_received=0, bonus_movement=0)