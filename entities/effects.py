from dataclasses import dataclass, field


@dataclass
class Effect:
    """
    A class that represents an effect.  

    `name` [str] is the name of the effect.  

    `damage` [int] is the amount of damage applied to a Pawn each turn. Negative values mean that the effect will heal each turn instead of damage.  

    `remaining_duration` [int|float("inf")] is the duration (in turns) of the effect. Duration will be counted down by the Board. The default duration is infinite (`float("inf")`).  

    `change_damage_dealt` [int] is an amount of bonus damage that the Pawn this effect is applied to can deal while it has this effect. Positive values add bonus damage to a Pawn's attack, negative values decrease the Pawn's damage. The default value is zero.  

    `change_movement` [int] is an integer amount of bonus grid squares that the pawn will be able to move each turn. See the Haste effect for an example of this. Positive values will increase the number of squares that a Pawn can move, and negative values will decrease the number of squares. The default value is zero.  

    `change_max_health` [int] is the amount of hit points added to the Pawn's maximum hit points when this effect is applied. A positive number will increase the Pawn's maximum hit points; a negative number will decrease the Pawn's hit points. The default value is zero.
    """
    name: str
    damage: int
    remaining_duration: int | float = field(default=float("inf"), hash=False)
    change_damage_dealt: int = field(default=0, hash=False)
    change_movement: int = field(default=0, hash=False)
    change_max_health: int = field(default=0, hash=False)


# some examples of effects that can be applied to Pawns
# spells
Burning = Effect(name="Burning", damage=2, remaining_duration=3,
                 change_damage_dealt=0, change_movement=0)
Freezing = Effect(name="Freezing", damage=1, remaining_duration=3,
                  change_damage_dealt=0, change_movement=-1)

Haste = Effect(name="Haste", damage=0, remaining_duration=3,
               change_damage_dealt=0, change_movement=1)
Bless = Effect(name="Bless", damage=0, remaining_duration=3,
               change_damage_dealt=1, change_movement=0)

# Equipment effects
Curse = Effect(name="Curse", damage=0, remaining_duration=float(
    'inf'), change_damage_dealt=-1, change_movement=0)
