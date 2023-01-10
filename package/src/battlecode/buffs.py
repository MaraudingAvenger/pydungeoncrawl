#
# BUFFS

# ❤ (Cleric Heal)
# 💕 (Druid Heal)
# 💗 (Shaman Heal)
# 💖 (Used Cure)
# ⚡ (Used Stun?)
# 💙 (Has Heal over Time effect)
# 💚 (has DoT that can be cured)
# 🌀 (stunned)
# 🐌 (rooted) or 🌳
# 👀 (blind)
# ⚔ (attacked)
# 🦶 (moved)
# ❄ (has Frost exhaustion)
# 🔥 (has Fire exhaustion)
# ⚙ (other)

# 🥶 frost
# 🥵 fire
# 😵 stun
# 🤐 silence
# 🤢 sick/poison
# 🤪 confusion
# 🥴 weak
# 😑 blind

# Might (stacking) – Increase damage done by 5%
# Toughness (stacking) – Reduces damage received by 5%
# Next Attack – Increase damage done by X% on next attack (value on creation)
# Barrier – Absorb and store all damage for X turns (owned by caster,  object passed)
# Reflect – Reflect 50% of damage received back to target (can receive increasing modifiers)
# Parry – Completely avoid an attack
#!!-- Cure – Remove negative ailments from the target!!
# Shield Stance - Reduce damage by 75% for 3 turns. Prevents any action during this time. At the end receive 5 stacks of Toughness for each hit taken while Shield Stance was active.
#

from typing import Union
from .entities.characters import Party
from .entities.pawn import Pawn
from .entities.effects import Effect

from .debuffs import ExposeWeakness


class Parry(Effect):
    def __init__(self, user: Pawn, duration: Union[int,float] = float('inf')) -> None:
        super().__init__(name="Parry", duration=duration, take_bonus_damage_percent=-1.0,
                         category={'physical', 'buff', 'parry', 'defense', 'defensive', 'reflect'}, symbol='🖕')
        self.user = user
        self.user.effects.remove_name("might")
        self.user.effects.remove_name("expose weakness")

    def on_activate(self, *args, **kwargs) -> None:
        print('Parry activated'* 50)
        if isinstance((damager := kwargs.get('damager')), Pawn) and kwargs.get("total_damage", 0) > 0:
            self.duration = 0
            self.user.effects.add_stacks(Toughness, stacks=2, duration=3)
            damager.effects.add_stacks(ExposeWeakness, stacks=4, duration=3)


class Might(Effect):
    def __init__(self, duration: Union[int,float]) -> None:
        super().__init__(name="Might", duration=duration, deal_bonus_damage_percent=.05,
                         category={'physical', 'buff', 'might', 'strength', 'offensive'}, symbol='💪')


class Toughness(Effect):
    def __init__(self, duration: Union[int,float]) -> None:
        super().__init__(name="Toughness", duration=duration, take_bonus_damage_percent=-.05,
                         category={'physical', 'buff', 'tough', 'toughness', 'defense', 'defensive', 'modifier'}, symbol='✊')

class HoT(Effect):
    def __init__(self, name: str, duration:int=3, heal_amount:int=3) -> None:
        super().__init__(name=name, duration=duration, heal_over_time=heal_amount, category={'hot', 'buff', 'heal', 'heal over time'}, symbol='💕')

class CurativeNotes(Effect):
    def __init__(self, target: Pawn) -> None:
        self.target = target
        super().__init__(name="Curative Notes", duration=2,
                         category={'cure', 'buff'}, symbol='💊')

    def on_expire(self) -> None:
        self.target.effects.remove_all(
            *self.target.effects.get_damage_over_time_effects())


class NextAttack(Effect):
    def __init__(self, damage_percent: float) -> None:
        super().__init__(name="Next Attack", duration=float('inf'), deal_bonus_damage_percent=damage_percent,
                         category={'physical', 'buff', 'next attack', 'offense', 'offensive'}, symbol='💢')

    def on_activate(self, *args, **kwargs) -> None:
        self.duration = 0


class Barrier(Effect):
    def __init__(self, caster: Pawn, duration) -> None:
        super().__init__(name="Barrier", duration=duration, category={
            'physical', 'buff', 'barrier', 'shield', 'defense', 'defensive'}, symbol='🤍')
        self.caster = caster

    def on_activate(self, *args, **kwargs) -> None:
        self.caster.reports.setdefault('barrier', 0)
        self.caster.reports['barrier'] += kwargs.get("total_damage", 0)


class DivineProtection(Effect):
    def __init__(self, caster: Pawn, duration) -> None:
        super().__init__(name="Divine Protection", duration=duration, category={
            'physical', 'buff', 'barrier', 'shield', 'defense', 'defensive'}, symbol='🤍')
        self.caster = caster

    def on_activate(self, *args, **kwargs) -> None:
        self.caster.reports.setdefault('barrier', 0)
        self.caster.reports['barrier'] += kwargs.get("total_damage", 0)
        self.duration = 0


class Reflect(Effect):
    def __init__(self, duration: Union[int,float], extra: float = 0.) -> None:
        percent = .5 + extra
        super().__init__(name="Reflect", duration=duration, category={
            'physical', 'buff', 'reflect', 'defense', 'offense', 'defensive', 'offensive'}, symbol='♻', reflect_damage_percent=percent,)


class ShieldStance(Effect):
    def __init__(self, user: Pawn) -> None:
        super().__init__(name="Shield Stance", duration=3, category={
            'physical', 'buff', 'shield stance', 'shield', 'defense', 'defensive', 'damage_activate'}, symbol='🔰')
        self.user = user
        self.user.reports['shield stance'] = 0

    def on_activate(self, *args, **kwargs) -> None:
        self.user.reports['shield stance'] += 1

    def on_expire(self) -> None:
        times = self.user.reports.get('shield stance', 0) * 5
        self.user.effects.add_stacks(Toughness, stacks=times, duration=3)


class Inspiration(Effect):
    def __init__(self, party: Party) -> None:
        super().__init__(name="Inspiration", duration=5, category={
            'physical', 'buff', 'inspiration', 'offense', 'offensive', 'damage_activate'}, symbol='🎶')
        self.party = party

    def on_activate(self, *args, **kwargs) -> None:
        for member in self.party:
            member._heal(kwargs.get("total_damage", 0))
            member.effects.add(Toughness(5))
