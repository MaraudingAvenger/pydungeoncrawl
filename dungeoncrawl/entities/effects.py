from dataclasses import dataclass, field


@dataclass
class Effect:
    """
    A class that represents an effect.  

    `name` [str] is the name of the effect.  

    `duration` [int|float("inf")] This indicates the number of turns that the effect will remain active. The default duration is infinite (`float("inf")`).  

    `bonus_damage` [int] This affects the amount of damage that the bearer of the effect deals. Positive values increase damage, negative values decrease damage.

    `bonus_damage_received` [int] This affects the amount of damage that the bearer of the effect will receive. Positive values increase the damage that the bearer receives, negative values decrease it.  

    `bonus_movement` [int] is an integer amount of bonus grid squares that the pawn will be able to move each turn. See the Haste effect for an example of this. Positive values will increase the number of squares that a Pawn can move, and negative values will decrease the number of squares. The default value is zero.  

    `bonus_max_health` [int] is the amount of hit points added to the Pawn's maximum hit points when this effect is applied. A positive number will increase the Pawn's maximum hit points; a negative number will decrease the Pawn's hit points. The default value is zero.
    """
    name: str
    duration: int | float = field(default=float("inf"), hash=False)
    bonus_damage: int = field(default=0, hash=False)
    bonus_damage_received: int = field(default=0, hash=False)
    bonus_movement: int = field(default=0, hash=False)
    bonus_max_health: int = field(default=0, hash=False)


class Effects:
    '''
    Convenience class for a collection of effects.

    `add()`, `remove()` add or remove effects from the collection.

    `tick()` decrements the duration of the effects in the collection.

    `bonus_damage`, `bonus_damage_received`, `bonus_movement`, and`bonus_max_health` are all the collected values of the effects in the collection.
    '''

    def __init__(self):
        self._effects: list[Effect] = []

    def add(self, effect: Effect) -> None:
        self._effects.append(effect)

    def remove(self, effect: Effect) -> None:
        self._effects.remove(effect)

    def tick(self) -> None:
        rm = []
        for i, effect in enumerate(self._effects):
            effect.duration -= 1
            if effect.duration <= 0:
                rm.append(i)
        for i in rm[::-1]:
            self._effects.pop(i)

    @property
    def active(self):
        return len(self._effects) > 0

    @property
    def bonus_damage(self) -> int:
        return sum(effect.bonus_damage for effect in self._effects)

    def get_damage_effects(self) -> list[Effect]:
        return [effect for effect in self._effects if effect.bonus_damage != 0]

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
Burning = Effect(name="Burning", duration=3, bonus_damage=2,
                 bonus_damage_received=0, bonus_movement=0)
Freezing = Effect(name="Freezing", bonus_damage=1, duration=3,
                  bonus_damage_received=0, bonus_movement=-1)

Haste = Effect(name="Haste", duration=3, bonus_damage=0,
               bonus_damage_received=0, bonus_movement=1)
Bless = Effect(name="Bless", bonus_damage=0, duration=3,
               bonus_damage_received=-1, bonus_movement=0)

# Equipment effects
Curse = Effect(name="Curse", duration=float('inf'),
               bonus_damage=-1, bonus_damage_received=1, bonus_movement=0)
Fire = Effect(name="Fire", bonus_damage=2, duration=0,
              bonus_damage_received=0, bonus_movement=0)
