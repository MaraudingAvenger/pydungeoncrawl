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

from dungeoncrawl.bosses import Boss
from dungeoncrawl.entities.pawn import Pawn
from dungeoncrawl.entities.effects import Effect
from dungeoncrawl.debuffs import ExposeWeakness


class Parry(Effect):
    def __init__(self, user: Pawn, boss:Boss) -> None:
        super().__init__(name="Parry", duration = float('inf'), take_bonus_damage_percent=-1.0)
        self.user = user
        self.boss = boss

    def on_activate(self, *args, **kwargs) -> None:
        if kwargs.get("total_damage", 0) > 0:
            self.duration = 0
            self.user.effects.remove_all("might")
            self.user.effects.remove_all("expose weakness")
            for _ in range(4):
                self.boss.effects.add(ExposeWeakness())
