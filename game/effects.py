from dataclasses import dataclass, field

@dataclass
class Effect:
    name:str
    damage:int
    remaining_duration:int|float = field(default=float("inf"), hash=False)
    change_damage_dealt:int= field(default=0, hash=False)
    change_movement:int= field(default=0, hash=False)
    change_max_health:int= field(default=0, hash=False)


# some examples of effects that can be applied to Pawns
# spells
Burning = Effect(name="Burning", damage=2, remaining_duration=3, change_damage_dealt=0, change_movement=0)
Freezing = Effect(name="Freezing", damage=1, remaining_duration=3, change_damage_dealt=0, change_movement=-1)

Haste = Effect(name="Haste", damage=0, remaining_duration=3, change_damage_dealt=0, change_movement=1)
Bless = Effect(name="Bless", damage=0, remaining_duration=3, change_damage_dealt=1, change_movement=0)

# Equipment effects
Curse = Effect(name="Curse", damage=0, remaining_duration=float('inf'), change_damage_dealt=-1, change_movement=0)
