#
# BUFFS
# Might (stacking) – Increase damage done by 5%
# Toughness (stacking) – Reduces damage received by 5%
# Next Attack – Increase damage done by X% on next attack (value on creation)
# Barrier – Absorb and store all damage for X turns (owned by caster,  object passed)
# Reflect – Reflect 50% of damage received back to target (can receive increasing modifiers)
# Parry – Completely avoid an attack
#!!-- Cure – Remove negative ailments from the target!!
# Shield Stance - Reduce damage by 75% for 3 turns. Prevents any action during this time. At the end receive 5 stacks of Toughness for each hit taken while Shield Stance was active.
#

from pawn import Pawn
from effects import Effect


class Might(Effect):
    def __init__(self, duration: int | float = float('inf'), atk_mod_pct: float = 0.05) -> None:
        super().__init__(name="Might", duration=duration,
                         category="buff", bonus_damage_output_percent=atk_mod_pct)


class Toughness(Effect):
    def __init__(self, duration: int | float = float('inf'), def_mod_pct: float = -0.05) -> None:
        super().__init__(name="Toughness", duration=duration,
                         category="buff", bonus_damage_received_percent=def_mod_pct)


class NextAttack(Effect):
    def __init__(self, duration: int | float = float('inf'), atk_mod_pct: float = 0.1) -> None:

        def on_use(self) -> None:
            self.duration = 0

        super().__init__(name="Next Attack", duration=duration, category="buff",
                         bonus_damage_output_percent=atk_mod_pct, on_use=on_use)


class Barrier(Effect):
    def __init__(self, owner:Pawn, duration: int | float = float('inf')) -> None:
        self.absorbed_damage = 0
        self.owner = owner

        def on_use(self, damage) -> None:
            self.absorbed_damage += damage
        
        def on_deactivate(self) -> None:
            #TODO: Name this function whatever it's called on the classes
            self.owner.report_absorbed_damage(self.absorbed_damage)

        super().__init__(name="Barrier", duration=duration, category="buff", on_use=on_use, on_deactivate=on_deactivate)


class Reflect(Effect):
    def __init__(self, duration: int | float = float('inf'), reflect_pct: float = 0.5) -> None:
        self.reflect_pct = reflect_pct

        def on_use(self, damage) -> None:
            return damage * self.reflect_pct

        super().__init__(name="Reflect", duration=duration, category="buff", on_use=on_use)


class Parry(Effect):
    def __init__(self, duration: int | float = float('inf'), dmg_reduct_pct=-1.) -> None:

        def on_use(self) -> None:
            self.duration = 0

        super().__init__(name="Parry", duration=duration, category="buff",
                         on_use=on_use, bonus_damage_received_percent=dmg_reduct_pct)
        
class ShieldStance(Effect):
    def __init__(self, duration: int | float = float('inf'), dmg_reduct_pct=-0.75, toughness_stacks=0) -> None:
        self.toughness_stacks = toughness_stacks

        def on_use(self) -> None:
            self.duration = 0

        def on_deactivate(self) -> None:
            self.owner.effects.add(Toughness(duration=float('inf'), def_mod_pct=self.toughness_stacks * -0.05))

        super().__init__(name="Shield Stance", duration=duration, category="buff",
                         on_use=on_use, on_deactivate=on_deactivate, bonus_damage_received_percent=dmg_reduct_pct)

