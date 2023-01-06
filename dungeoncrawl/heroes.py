from dungeoncrawl.entities.pawn import Pawn, _action_decorator
from dungeoncrawl.entities.characters import Character, Party
from dungeoncrawl.utilities.location import Point, bresenham

from dungeoncrawl.armor import *
from dungeoncrawl.weapons import *
from dungeoncrawl.buffs import *
from dungeoncrawl.debuffs import *


class Guardian(Character):
    def __init__(self, name: str) -> None:
        '''
        The Guardian is a tanky character that can take a lot of damage, but he isn't
        very good at dealing damage himself.
        '''
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
        "Strike the target and apply 2 stacks of Toughness to yourself."
        target._take_damage(self, self.calculate_damage(2, target), 'physical')
        self.effects.add_stacks(Toughness, stacks=2, duration=5)

    @_action_decorator(cooldown=10, affected_by_blind=True) # type: ignore
    def shield_stance(self) -> None:
        """
        Take on a defensive stance reducing damage you receive by 75% for 3 turns.
        However, the Guardian cannot take any action during this time. At the end you
        will receive 5 stacks of Toughness for each hit taken.
        """
        self.effects.add(Stun(3))
        self.effects.add(ShieldStance(self))

    @_action_decorator(cooldown=5) # type: ignore
    def shield_spike(self) -> None:
        """
        Give yourself 50% Reflect for 2 turns. Consumes your Toughness and adds
        it to the Reflect amount.
        """
        extra = self.effects.count('Toughness') * 0.05
        self.effects.add(Reflect(2, extra))
        self.effects.remove_name('Toughness')

    @_action_decorator(cooldown=10, melee=True, affected_by_blind=True) # type: ignore
    def shield_bash(self, target: Pawn) -> None:
        """
        Bash the target with your shield and apply Stun for 1 turn.
        """
        target._take_damage(self, self.calculate_damage(10, target), 'physical')
        target.effects.add(Stun(1))

    @_action_decorator(cooldown=100) # type: ignore
    def inspiration(self, party: Party) -> None:
        """
        All damage the Guardian receives will instead heal the Party and apply
        1 stack of Toughness for 5 turns.
        """
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
            target.effects.add_stacks(Frailty, stacks=5, duration=3)
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


class Ranger(Character):
    '''
    Ranger 
    Shoot (Damage, Physical, Debuff) – Fire an arrow from anywhere in the arena. Damage increased by distance. 3 shots in a row will apply 1 stack of Expose Weakness for 2 turns. 
    Virulent Arrow (Damage, Physical, DoT, Poison, Debuff) – Fire a Poison arrow. If the target is not currently affected by a poison, virulent arrow applies Poison Vulnerability for 3 turns. 
    Frostfire Arrow (Damage, Physical, Debuff) – Fire an elemental arrow. If the target does not have Fire Resistance or Frost Resistance, frostfire arrow applies 3 stacks of Magic Vulnerability. 
    Field Medicine (Heal, Cure) – Instantly Heal the target for 20% and apply Cure. 
    Murder (DoT, Debuff) – Send a murder of crows to claw at the target defenses applying Blind and 6 stacks of Expose Weakness for 3 turns.
    '''
    def __init__(self, name:str):
        symbol: str = '🏹'
        role: str='dps'
        position: Point | tuple[int, int] = Point(0, 0)
        health_max: int = 100
        gear = LeatherArmor()
        super().__init__(name=name, symbol=symbol, role=role, position=position, health_max=health_max, gear=gear)
        self.equip(ShortBow())
        self.reports['shots'] = 0

    @_action_decorator(melee=False, affected_by_blind=True) #type: ignore
    def shoot(self, target: Pawn) -> None:
        dmg = self.calculate_damage(len(list(bresenham(self.position, target.position))), target)
        self.reports['shots'] += 1
        if self.reports['shots'] >= 3:
            target.effects.add(ExposeWeakness(2))
        target._take_damage(self, dmg, "physical")

    @_action_decorator(cooldown=5, melee=False, affected_by_blind=True) #type: ignore
    def virulent_arrow(self, target: Pawn) -> None:
        self.reports['shots'] = 0
        if not target.poisoned:
            target.effects.add(PoisonVulnerability(3))
        target.effects.add(Poison(target, duration=3, dot_amount=5))
        target._take_damage(self, self.calculate_damage(10, target), "physical")

    @_action_decorator(cooldown=10, melee=False, affected_by_blind=True) #type: ignore
    def frostfire_arrow(self, target: Pawn) -> None:
        self.reports['shots'] = 0
        if not target.has_effect(FireResistance()) and not target.has_effect(FrostResistance()):
            target.effects.add_stacks(MagicVulnerability, stacks=3)
        target._take_damage(self, self.calculate_damage(10, target), "physical")

    @_action_decorator(cooldown=5, melee=False) #type: ignore
    def field_medicine(self, target: Pawn) -> None:
        self.reports['shots'] = 0
        target._heal(self.calculate_damage(target.health_max//5, target))
        target.effects.remove_category('debilitating')
        target.effects.remove_category('vulnerable')
        target.effects.remove_category('dot')

    @_action_decorator(cooldown=100, melee=False) #type: ignore
    def murder(self, target: Pawn) -> None:
        'Send a murder of crows to enact judgement on a target.'
        self.reports['shots'] = 0
        target.effects.add(Blind(4))
        target.effects.add_stacks(ExposeWeakness, stacks=6, duration=4)
        target.effects.add(DoT(target, name="Murder of Crows", duration=4, dot_amount=self.calculate_damage(10, target)))


class Rogue(Character):
    '''
    Rogue 
    Backstab (Damage, Physical, Debuff) – Stab the target. Deals double damage when used from behind. 3 double damage backstabs in a row will apply 2 stacks of Expose Weakness to the target for 2 turns.
    Poison Sick (DoT, Poison) – Apply poison to the target and 4 stacks of Frailty for 4 turns. 
    Sand (Debuff) – Blind the target this turn
    Shank (Damage, Debuff) – Stab the target and twist the blade. Doubles the stacks of Expose Weakness and Magic Vulnerability on the target. 
    Ambush (Damage, Debuff, Poison) – Quadruple damage backstab that applies Blind for 2 turns and Poison Vulnerability plus 4 stacks of Frailty for 5 turns. 
    '''
    def __init__(self, name) -> None:
        symbol: str = '🗡️'
        role: str='dps'
        position: Point | tuple[int, int] = Point(0, 0)
        health_max: int = 100
        gear = LeatherArmor()
        super().__init__(name=name, symbol=symbol, role=role, position=position, health_max=health_max, gear=gear)
        self.equip(Dagger())
        self.equip(SideKnife())
        self.reports['backstab'] = 0

    def is_behind(self, target: Pawn) -> bool:
        return self.position in target.points_behind

    @_action_decorator(melee=True, affected_by_blind=True) #type: ignore
    def backstab(self, target: Pawn) -> None:
        "Try doing it from behind!"
        dmg = self.calculate_damage(20, target)
        if self.is_behind(target):
            dmg *= 2
            self.reports['backstab'] += 1
            if self.reports['backstab'] >= 3:
                target.effects.add_stacks(ExposeWeakness, stacks=2, duration=3)
        target._take_damage(self, dmg, "physical")

    @_action_decorator(cooldown=5, melee=True) #type: ignore
    def envenom(self, target: Pawn) -> None:
        "Poisons and Enfeebles the target"
        self.reports['backstab'] = 0
        target.effects.add(Poison(target, duration=4, dot_amount=5))
        target.effects.add_stacks(Frailty, stacks=4, duration=4)
        if target.effects.vulnerable_to('poison'):
            target.effects.add_stacks(Frailty, stacks=4, duration=4)

    @_action_decorator(cooldown=10, melee=True) #type: ignore
    def sand(self, target: Pawn) -> None:
        "Go for the eyes!"
        self.reports['backstab'] = 0
        target.effects.add(Blind(1))
    
    @_action_decorator(cooldown=10, melee=True) #type: ignore
    def shank(self, target: Pawn) -> None:
        "Twist the knife!"
        self.reports['backstab'] = 0
        target.effects.add_stacks(ExposeWeakness, stacks=target.effects.count('expose_weakness'), duration=2)
        target.effects.add_stacks(MagicVulnerability, stacks=target.effects.count('magic vulnerability'))
        target._take_damage(self, self.calculate_damage(10, target), "physical")

    @_action_decorator(cooldown=100, melee=True) #type: ignore
    def ambush(self, target: Pawn) -> None:
        "Surprise!"
        target.effects.add(Blind(2))
        target.effects.add_stacks(Frailty, stacks=4, duration=10)
        target.effects.add(PoisonVulnerability(5))

        dmg = self.calculate_damage(40, target)
        if self.is_behind(target):
            dmg *= 2
            self.reports['backstab'] += 1
            if self.reports['backstab'] >= 3:
                target.effects.add_stacks(ExposeWeakness, stacks=2, duration=3)
        target._take_damage(self, dmg, "physical")