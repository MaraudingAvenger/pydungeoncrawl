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
    tick. The default value is zero.

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
    damage_over_time: int = field(default=0, hash=False)
    bonus_damage_output: int = field(default=0, hash=False)
    bonus_damage_received: int = field(default=0, hash=False)
    bonus_movement: int = field(default=0, hash=False)
    bonus_max_health: int = field(default=0, hash=False)


class Effects:
    '''
    Convenience class for a collection of effects.

    `add()`, `remove()` add or remove effects from the collection.

    `tick()` decrements the duration of the effects in the collection.

    `bonus_damage`, `bonus_damage_received`, `bonus_movement`, and`bonus_max_health` are all the collected
    values of the effects in the collection.
    '''

    def __init__(self):
        self._effects: dict[str,Effect] = {}

    def add(self, effect: Effect) -> None:
        'add an effect to the collection'
        if effect.name in self._effects:
            self._effects[effect.name].duration += effect.duration
        else:
            self._effects[effect.name] = effect

    @singledispatchmethod
    def remove(self, effect: Effect) -> None:
        'remove an effect from the collection'
        self._effects.pop(effect.name)
    
    @remove.register
    def _(self, effect_name: str) -> None:
        'remove an effect from the collection'
        self._effects.pop(effect_name)

    def tick(self) -> None:
        'decrement the duration of all effects in the collection'
        rm = []
        for effect in self._effects.values():
            effect.duration -= 1
            if effect.duration <= 0:
                rm.append(effect.name)
        for name in rm:
            self.remove(name)

    @property
    def active(self):
        return len(self._effects.keys()) > 0

    @property
    def damage_over_time(self) -> int:
        return sum(effect.damage_over_time for effect in self._effects.values())
    def get_damage_over_time_effects(self) -> list[Effect]:
        return [effect for effect in self._effects.values() if effect.damage_over_time != 0]
    def get_dot_effects(self) -> list[Effect]:
        'alias for `get_damage_over_time_effects()`'
        return self.get_damage_over_time_effects()

    @property
    def bonus_damage_output(self) -> int:
        return sum(effect.bonus_damage_output for effect in self._effects.values())
    def get_damage_output_effects(self) -> list[Effect]:
        return [effect for effect in self._effects.values() if effect.bonus_damage_output != 0]

    @property
    def bonus_movement(self) -> int:
        return sum(effect.bonus_movement for effect in self._effects.values())
    def get_movement_effects(self) -> list[Effect]:
        return [effect for effect in self._effects.values() if effect.bonus_movement != 0]

    @property
    def bonus_damage_received(self) -> int:
        return sum(effect.bonus_damage_received for effect in self._effects.values())
    def get_damage_received_effects(self) -> list[Effect]:
        return [effect for effect in self._effects.values() if effect.bonus_damage_received != 0]

    @property
    def bonus_max_health(self) -> int:
        return sum(effect.bonus_max_health for effect in self._effects.values())
    def get_max_health_effects(self) -> list[Effect]:
        return [effect for effect in self._effects.values() if effect.bonus_max_health != 0]


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
