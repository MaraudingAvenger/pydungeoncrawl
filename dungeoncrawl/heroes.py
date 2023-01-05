from dungeoncrawl.entities.pawn import Pawn, _action_decorator
from dungeoncrawl.entities.characters import Character, Party
from dungeoncrawl.utilities.location import Point

from dungeoncrawl.armor import *
from dungeoncrawl.weapons import *
from dungeoncrawl.buffs import *
from dungeoncrawl.debuffs import *


class Guardian(Character):
    '''
    Guardian
    Defensive Strike (Damage, Physical, Buff) - Strike the target and apply 2 stacks of Toughness to yourself.
    Shield Stance (Buff) - Take on a defensive stance reducing damage you receive by 75% for 3 turns but the Guardian cannot take any action during this time. At the end you will receive 5 stacks of Toughness for each hit taken.
    Shield Spike (Buff) - Give yourself 50% Reflect for 2 turns. Consumes your Toughness and adds it to the Reflect amount.
    Shield Bash (Damage, Physical, Debuff) Bash the target with your shield and apply Stun for 1 turn.
    Inspiration (Buff) - All damage the Guardian receives will instead heal the Party and apply 1 stack of Toughness for 5 turns.
    '''
    def __init__(self, name: str) -> None:
        symbol: str = '🛡️'
        role: str='tank'
        position: Point | tuple[int, int] = Point(0, 0)
        health_max: int = 100
        gear = PlateArmor()
        super().__init__(name=name, symbol=symbol, role=role, position=position, health_max=health_max, gear=gear)
        self.equip(Sword())
        self.equip(Shield())

    @_action_decorator(melee=True, affected_by_blind=True) # type: ignore
    def defensive_strike(self, target: Pawn) -> None:
        target._take_damage(self, self.calculate_damage(self._base_damage, target), 'physical')
        self.effects.add(Toughness(5), stacks=2)

    @_action_decorator(cooldown=10, affected_by_blind=True) # type: ignore
    def shield_stance(self) -> None:
        self.effects.add(Stun(3))
        self.effects.add(ShieldStance(self))

    @_action_decorator(cooldown=5) # type: ignore
    def shield_spike(self) -> None:
        extra = self.effects.count('Toughness') * 0.05
        self.effects.add(Reflect(2, extra))
        self.effects.remove_name('Toughness')

    @_action_decorator(cooldown=10, melee=True, affected_by_blind=True) # type: ignore
    def shield_bash(self, target: Pawn) -> None:
        target._take_damage(self, self.calculate_damage(self._base_damage, target), 'physical')
        target.effects.add(Stun(1))

    @_action_decorator(cooldown=100) # type: ignore
    def inspiration(self, party: Party) -> None:
        self.effects.add(Inspiration(party))

class Cleric(Character):
    '''
    Healing Word (Heal) – Instantly Heal the target for 50% health + stat modifier 
    Jolt (Magic, Debuff) – Apply Stun on the target for 2 turns. 3 turns if the target has Magic Vulnerability 
    Smite (Damage, Spirit, Debuff) – Smite the target and apply 1 stack of Frailty. Damage absorbed by Group Barrier is added and triggers 5 additional stacks of Frailty. 
    Cleanse (Cure) – Casts Cure on Target 
    Group Barrier (Barrier) – Barrier that absorbs 100% of damage received for 4 turns. All damage absorbed is used to empower your next Smite.
    '''

    def __init__(self, name: str) -> None:
        symbol: str = '🔅'
        role: str='healer'
        position: Point | tuple[int, int] = Point(0, 0)
        health_max: int = 100
        gear = PlateArmor()
        super().__init__(name=name, symbol=symbol, role=role, position=position, health_max=health_max, gear=gear)
        self.equip(Mace())
        self.equip(Shield())

    @_action_decorator
    def healing_word(self, target: Pawn) -> None:
        x = self.calculate_damage(target.health_max//2, target)
        target._heal(x)

    @_action_decorator(cooldown=10, affected_by_blind=True) # type: ignore
    def jolt(self, target: Pawn) -> None:
        if target.has_effect(MagicVulnerability()):
            target.effects.add(Stun(3))
            target.effects.remove_all(MagicVulnerability())
        else:
            target.effects.add(Stun(2))

    @_action_decorator(affected_by_blind=True) # type: ignore
    def smite(self, target: Pawn) -> None:
        if self.reports.get('barrier'):
            target.effects.add(Frailty(3), stacks=5)
            target._take_damage(self,
                self.calculate_damage(5, target) + self.reports['barrier'],
                'spirit')
            self.reports['barrier'] = 0
        else:
            target.effects.add(Frailty(3))
            target._take_damage(self, self.calculate_damage(5, target), 'spirit')

    @_action_decorator # type: ignore
    def cleanse(self, target: Pawn) -> None:
        target.effects.remove_category('debilitating')
        target.effects.remove_category('vulnerable')
        target.effects.remove_category('dot')

    @_action_decorator(cooldown=100) # type: ignore
    def group_barrier(self, party: Party) -> None:
        for member in party.members:
            member.effects.add(Barrier(self, 4))