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

from dungeoncrawl.bosses import Boss
from dungeoncrawl.entities.characters import Party
from dungeoncrawl.entities.pawn import Pawn
from dungeoncrawl.entities.effects import Effect
from dungeoncrawl.debuffs import ExposeWeakness


class Parry(Effect):
    def __init__(self, user: Pawn, boss: Boss) -> None:
        super().__init__(name="Parry", duration = float('inf'), take_bonus_damage_percent=-1.0, category={'physical', 'buff', 'parry', 'defense', 'defensive', 'reflect'}, symbol='🖕')
        self.user = user
        self.boss = boss
        self.user.effects.remove_name("might")
        self.user.effects.remove_name("expose weakness")


    def on_activate(self, *args, **kwargs) -> None:
        if kwargs.get("total_damage", 0) > 0:
            self.duration = 0
            self.boss.effects.add(ExposeWeakness(duration=3), stacks=4)

class Might(Effect):
    def __init__(self, duration: int) -> None:
        super().__init__(name="Might", duration = duration, deal_bonus_damage_percent=.05, category={'physical', 'buff', 'might', 'strength', 'offensive'}, symbol='💪')

class Toughness(Effect):
    def __init__(self, duration: int) -> None:
        super().__init__(name="Toughness", duration = duration, take_bonus_damage_percent=-.05, category={'physical', 'buff', 'tough', 'toughness', 'defense', 'defensive'}, symbol='✊')

class CurativeNotes(Effect):
    def __init__(self, target: Pawn) -> None:
        self.target = target
        super().__init__(name="Curative Notes", duration = 2, category={'cure', 'buff'}, symbol='💊')

    def on_expire(self) -> None:
        self.target.effects.remove_all(*self.target.effects.get_damage_over_time_effects())

class NextAttack(Effect):
    def __init__(self, damage_percent: float) -> None:
        super().__init__(name="Next Attack", duration=float('inf'), deal_bonus_damage_percent=damage_percent, category={'physical', 'buff', 'next attack', 'offense', 'offensive'}, symbol='💢')

    def on_activate(self, *args, **kwargs) -> None:
        self.duration = 0

class Barrier(Effect):
    def __init__(self, caster: Pawn, duration) -> None:
        super().__init__(name="Barrier", duration=duration, category={'physical', 'buff', 'barrier', 'shield', 'defense', 'defensive'}, symbol='🤍')
        self.caster = caster

    def on_activate(self, *args, **kwargs) -> None:
        self.caster.reports.setdefault('barrier', 0)
        self.caster.reports['barrier'] += kwargs.get("total_damage", 0)

class Reflect(Effect):
    def __init__(self, duration: int, extra:float = 0.) -> None:
        percent = .5 + extra
        super().__init__(name="Reflect", duration=duration, category={'physical', 'buff', 'reflect', 'defense', 'offense', 'defensive', 'offensive'}, symbol='♻', reflect_damage_percent=percent,)

class ShieldStance(Effect):
    def __init__(self, user: Pawn) -> None:
        super().__init__(name="Shield Stance", duration=3, category={'physical', 'buff', 'shield stance', 'shield', 'defense', 'defensive', 'damage_activate'}, symbol='🔰')
        self.user = user

    def on_activate(self, *args, **kwargs) -> None:
        print("shield stance has been activated")
        self.user.reports.setdefault('shield stance', 0)
        self.user.reports['shield stance'] += 1

    def on_expire(self) -> None:
        times = min([15, self.user.reports.get('shield stance', 0) * 5])
        self.user.effects.add(Toughness(duration=3), stacks=times)

class Inspiration(Effect):
    def __init__(self, party: Party) -> None:
        super().__init__(name="Inspiration", duration=5, category={'physical', 'buff', 'inspiration', 'offense', 'offensive', 'damage_activate'}, symbol='🎶')
        self.party = party

    def on_activate(self, *args, **kwargs) -> None:
        print("inspiration has been activated")
        self.party.tank.reports['butts'] = (args, kwargs)
        for member in self.party:
            print(f"{member.name} is inspired for {kwargs.get('total_damage', 0)}!")
            member._heal(kwargs.get("total_damage", 0))
            member.effects.add(Toughness(5))