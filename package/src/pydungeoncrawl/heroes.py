import math
import random
from typing import Union, Tuple

from .entities.pawn import Pawn, _action_decorator
from .entities.characters import Character, Party
from .utilities.location import Point, bresenham, get_adjacent_points

from .armor import ClothArmor, LeatherArmor, PlateArmor, ChainmailArmor, Shield
from .weapons import Sword, Claymore, Mace, Dagger, Staff, ShortBow, Wand, SideKnife, Lute

from .buffs import *
from .debuffs import * 


###############
# ~~ TANKS ~~ #
###############

class Guardian(Character):
    def __init__(self, name: str) -> None:
        '''
        The Guardian class can take a lot of damage, but isn't very good at dealing damage itself.
        '''
        symbol: str = '🛡️'
        role: str='tank'
        position: Union[Point,Tuple[int, int]] = Point(0, 0)
        health_max: int = 110
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
        You are unable to take any action during this time. At the end you
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


class Paladin(Character):
    def __init__(self, name: str) -> None:
        '''
        Powerful holy warrior that strikes a balance between offense and defense.
        
        '''
        symbol: str = '⚜️'
        role: str='tank'
        position: Union[Point,Tuple[int,int]] = Point(0, 0)
        health_max: int = 120
        gear = PlateArmor()
        super().__init__(name=name, symbol=symbol, role=role, position=position, health_max=health_max, gear=gear)
        self.equip(Sword())
        self.equip(Shield())
    
    @_action_decorator(melee=True, affected_by_blind=True) # type: ignore
    def holy_strike(self, target: Pawn) -> None:
        'Strike the target and apply 1 stack of Frailty.'
        target._take_damage(self, self.calculate_damage(5, target), 'physical')
        target.effects.add(Frailty(5))

    @_action_decorator(cooldown=5, affected_by_blind=False) # type: ignore
    def exorcise(self, target: Pawn) -> None:
        '''
        consume all stacks of Frailty to give yourself double the
        stacks in Toughness for 3 turns
        '''
        target._take_damage(self, self.calculate_damage(10, target), 'spirit')
        stacks = target.effects.count('Frailty')
        self.effects.add_stacks(Toughness, stacks=stacks*2, duration=3)
        target.effects.remove_name('Frailty')

    @_action_decorator(cooldown=10, affected_by_blind=False) # type: ignore
    def divine_protection(self, target: Pawn) -> None:
        '''
        Apply a Barrier to target or self to absorb the next hit and store the damage.
        '''
        target.effects.add(DivineProtection(caster=self, duration=10))

    @_action_decorator(cooldown=10, affected_by_blind=False) # type: ignore
    def prayer(self, party: Party) -> None:
        '''
        Remove all stacks of Toughness and buff the Party increasing the power of their next attack by the amount of Toughness consumed.
        '''
        stacks = self.effects.count('Toughness')
        self.effects.remove_name('Toughness')
        for member in party:
            member.effects.add(NextAttack(0.05 * stacks))

    @_action_decorator(cooldown=100, affected_by_blind=False) # type: ignore
    def holy_nova(self, target: Pawn, party: Party) -> None:
        '''
        Damage absorbed by Holy Barrier is used to trigger a holy nova on your target dealing damage and healing all Party members. Applies your Toughness stacks to the group for 5 turns.
        '''
        barrier = self.calculate_damage(self.reports.get('barrier', 0), target)
        self.reports['barrier'] = 0
        stacks = self.effects.count('Toughness')
        self.effects.remove_name('Toughness')
        for member in party:
            member.effects.add_stacks(Toughness, stacks=stacks, duration=5)
            member._heal(barrier)

        target._take_damage(self, barrier, 'spirit')

    
class Berzerker(Character):
    def __init__(self, name:str) -> None:
        symbol: str = '⚔️'
        role: str='tank'
        position: Union[Point,Tuple[int,int]] = Point(0, 0)
        health_max: int = 150
        gear = ChainmailArmor()
        super().__init__(name=name, symbol=symbol, role=role, position=position, health_max=health_max, gear=gear)
        self.equip(Claymore())

    @_action_decorator(cooldown=10, affected_by_root=True, affected_by_blind=True) # type: ignore
    def charge(self, target: Pawn) -> None:
        'Charge to the front of the target in a single turn.'
        self._teleport(target.facing_direction)
        self.face(target.position)

    @_action_decorator(melee=True, affected_by_blind=True) # type: ignore
    def frenzied_attack(self, target: Pawn) -> None:
        'Attack the target with no regard for your own safety. Apply 1 stack of Might and Expose Weakness to self.'
        target._take_damage(self, self.calculate_damage(15, target), 'physical')
        self.effects.add(Might(float('inf')))
        self.effects.add(ExposeWeakness(float('inf')))
    
    @_action_decorator(cooldown=10, melee=True, affected_by_blind=True) # type: ignore
    def rampage(self, target: Pawn) -> None:
        '''
        A devastating attack that applies 4 stacks of Might and Expose Weakness to yourself but cripples the enemy and applies 4 stacks of Magic Vulnerability, Expose Weakness,  and also Poison Vulnerability.
        '''
        self.effects.add_stacks(Might, stacks=4, duration=float('inf'))
        self.effects.add_stacks(ExposeWeakness, stacks=4, duration=float('inf'))

        target._take_damage(self, self.calculate_damage(30, target), 'physical')
        target.effects.add_stacks(PoisonVulnerability, stacks=4, duration=2)
        target.effects.add_stacks(ExposeWeakness, stacks=4, duration=2)
        target.effects.add_stacks(MagicVulnerability, stacks=4)

    @_action_decorator(cooldown=10, affected_by_blind=True) # type: ignore
    def parry(self) -> None:
        self.effects.add(Parry(user=self, duration=1))

    @_action_decorator(cooldown=100, affected_by_blind=False) # type: ignore
    def battle_shout(self, party: Party) -> None:
        stacks = self.effects.count('Might')
        self.effects.remove_name('Might')
        for member in party:
            member.effects.add_stacks(Might, stacks=stacks, duration=10)

    
#################
# ~~ HEALERS ~~ #
#################

class Cleric(Character):
    '''
    A dedicated healer that can heal and cleanse the party of debuffs. 
    '''

    def __init__(self, name: str) -> None:
        symbol: str = '🔅'
        role: str='healer'
        position: Union[Point,Tuple[int, int]] = Point(0, 0)
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
                self.calculate_damage(10, target) + self.reports['barrier'],
                'spirit')
            self.reports['barrier'] = 0
        else:
            target.effects.add(Frailty(3))
            target._take_damage(self, self.calculate_damage(5, target), 'spirit')

    @_action_decorator # type: ignore
    def cleanse(self, target: Pawn) -> None:
        target.effects.remove_category('curable')

    @_action_decorator(cooldown=100) # type: ignore
    def group_barrier(self, party: Party) -> None:
        for member in party.members:
            member.effects.add(Barrier(self, 4))


class Druid(Character):
    def __init__(self, name:str) -> None:
        symbol: str = '☘️'
        role: str='healer'
        position: Union[Point,Tuple[int,int]] = Point(0, 0)
        health_max: int = 100
        gear = LeatherArmor()
        super().__init__(name=name, symbol=symbol, role=role, position=position, health_max=health_max, gear=gear)
        self.equip(Staff())

    @_action_decorator(affected_by_blind=False) # type: ignore
    def swift_mend(self, target: Pawn) -> None:
        heal_amount = self.calculate_damage(target.health_max//3, target)
        target._heal(heal_amount)
        target.effects.add(HoT(name="Swift Mend", duration=2, heal_amount=heal_amount//2))
    
    @_action_decorator(cooldown=10, affected_by_blind=True) # type: ignore
    def grasping_roots(self, target: Pawn) -> None:
        target.effects.add(Root(4))
        if target.has_effect(MagicVulnerability()):
            target.effects.add_stacks(ExposeWeakness, stacks=5, duration=3)
            target.effects.remove_all(MagicVulnerability())

    @_action_decorator(affected_by_blind=True) # type: ignore
    def blaze(self, target: Pawn) -> None:
        '''
        Blasts the target with intense heat and apply 1
        stack of Expose Weakness and Fire Resistance
        '''
        target._take_damage(self, self.calculate_damage(10, target), 'fire')
        target.effects.add(FireResistance())
        target.effects.add(ExposeWeakness(3))

    @_action_decorator(affected_by_blind=True) # type: ignore
    def salve(self, target: Pawn) -> None:
        'Remove all curable effects from target'
        target.effects.remove_category('curable')

    @_action_decorator(cooldown=100) # type: ignore
    def group_thornshield(self, party: Party) -> None:
        'Apply Reflect and Toughness to party for 8 turns'
        for member in party.members:
            member.effects.add(Reflect(8))
            member.effects.add_stacks(Toughness, stacks=5, duration=8)


class Shaman(Character):
    def __init__(self, name:str) -> None:
        symbol: str = '🍄'
        role: str='healer'
        position: Union[Point,Tuple[int,int]] = Point(0, 0)
        health_max: int = 100
        gear = ChainmailArmor()
        super().__init__(name=name, symbol=symbol, role=role, position=position, health_max=health_max, gear=gear)
        self.equip(Staff())

    @_action_decorator(affected_by_blind=False) # type: ignore
    def regenerate(self, target: Pawn) -> None:
        'Heal target for 80% of their health max over 5 turns'
        heal_amount = self.calculate_damage(target.health_max // 5 * 4, target)
        target.effects.add(HoT(name="Regenerate", duration=5, heal_amount=heal_amount//5))

    @_action_decorator(cooldown=5, affected_by_blind=True) # type: ignore
    def enhancement(self, target: Pawn) -> None:
        'Apply 5 stacks of Might and Toughness to the target for 3 turns'
        target.effects.add_stacks(Might, stacks=5, duration=3)
        target.effects.add_stacks(Toughness, stacks=5, duration=3)

    @_action_decorator(cooldown=2, affected_by_blind=True) # type: ignore
    def poison_frost(self, target: Pawn) -> None:
        '''
        Apply a frost based poison to the target, 2 stacks of
        Frailty, and 1 stack of Frost Resistance
        '''
        target.effects.add(Poison(target, 4, self.calculate_damage(4, target)))
        target.effects.add_stacks(Frailty, stacks=2, duration=4)
        target.effects.add(FrostResistance())
        if target.vulnerable_to('poison'):
            target.effects.add(Poison(target, 4, self.calculate_damage(4, target)))
            target.effects.add_stacks(Frailty, stacks=2, duration=4)
            target.effects.add(FrostResistance())
    
    @_action_decorator(affected_by_blind=False) # type: ignore
    def purge(self, target: Pawn) -> None:
        'Remove all curable effects from target'
        target.effects.remove_category('curable')

    @_action_decorator(cooldown=100) # type: ignore
    def group_infusion(self, party: Party) -> None:
        'Apply 10 stacks of Might to Party for 8 turns'
        for member in party.members:
            member.effects.add_stacks(Might, stacks=10, duration=8)

    

#############
# ~~ DPS ~~ #
#############

class Ranger(Character):
    def __init__(self, name:str):
        symbol: str = '🏹'
        role: str='dps'
        position: Union[Point,Tuple[int,int]] = Point(0, 0)
        health_max: int = 80
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
        self.reports['shots'] += 1
        if not target.poisoned:
            target.effects.add(PoisonVulnerability(3))
        target.effects.add(Poison(target, duration=3, dot_amount=5))
        target._take_damage(self, self.calculate_damage(10, target), "physical")

    @_action_decorator(cooldown=10, melee=False, affected_by_blind=True) #type: ignore
    def frostfire_arrow(self, target: Pawn) -> None:
        self.reports['shots'] += 1
        if not target.has_effect(FireResistance()) and not target.has_effect(FrostResistance()):
            target.effects.add_stacks(MagicVulnerability, stacks=3)
        target._take_damage(self, self.calculate_damage(10, target), "physical")

    @_action_decorator(cooldown=5, melee=False) #type: ignore
    def field_medicine(self, target: Pawn) -> None:
        self.reports['shots'] = 0
        target._heal(self.calculate_damage(target.health_max//5, target))
        target.effects.remove_category('curable')

    @_action_decorator(cooldown=100, melee=False) #type: ignore
    def murder(self, target: Pawn) -> None:
        'Send a murder of crows to enact judgement on a target.'
        self.reports['shots'] = 0
        target.effects.add(Blind(4))
        target.effects.add_stacks(ExposeWeakness, stacks=6, duration=4)
        target.effects.add(DoT(target, name="Murder of Crows", duration=4, dot_amount=self.calculate_damage(10, target)))


class Rogue(Character):
    def __init__(self, name) -> None:
        symbol: str = '🗡️'
        role: str='dps'
        position: Union[Point,Tuple[int,int]] = Point(0, 0)
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
            dmg *= 10
            self.reports['backstab'] += 1
            if self.reports['backstab'] >= 3:
                target.effects.add_stacks(ExposeWeakness, stacks=2, duration=3)
        target._take_damage(self, dmg, "physical")


class Necromancer(Character):
    def __init__(self, name: str) -> None:
        symbol: str = '🦴'
        role: str='dps'
        position: Union[Point,Tuple[int,int]] = Point(0, 0)
        health_max: int = 80
        gear = ClothArmor()
        super().__init__(name=name, symbol=symbol, role=role, position=position, health_max=health_max, gear=gear)
        self.equip(Wand())
    
    @_action_decorator(melee=False) #type: ignore
    def poison_blast(self, target: Pawn) -> None:
        '''
        Blast the target with Poison and apply 1 stack of Expose Weakness
        '''
        target._take_damage(self, self.calculate_damage(20, target), "poison")
        target.effects.add_stacks(ExposeWeakness, stacks=1, duration=4)

    @_action_decorator(cooldown=10, melee=False) #type: ignore
    def doom(self, target: Pawn) -> None:
        '''
        Consume and combine the negative effects on the target into a delayed damage effect that triggers 15 turns. 
        '''
        doom = target.effects.find_effect_exact_text('doom')
        if doom:
            doom.increase_doom() # type: ignore
        else:
            target.effects.add(Doom(self, target, self.calculate_damage(10, target)))

    @_action_decorator(melee=False) #type: ignore
    def blood_magic(self, target: Pawn, sacrifice: int) -> None:
        '''
        Sacrifice health to damagea target. 
        '''
        if sacrifice > self.health:
            sacrifice = self.health
        target._take_damage(self, self.calculate_damage(sacrifice, target), "spirit")
        self.health -= sacrifice

    @_action_decorator(cooldown=10, melee=False) #type: ignore
    def life_tap(self, target: Pawn) -> None:
        '''
        Leach health from the target and transfer it to yourself and apply 2 stacks of Expose Weakness. If the target has Magic Vulnerability apply Poison Vulnerability for 5 turns.
        '''
        dmg = self.calculate_damage(20, target)
        target._take_damage(self, dmg, "spirit")
        self._heal(dmg)
        target.effects.add_stacks(ExposeWeakness, stacks=2, duration=4)
        if target.effects.vulnerable_to('magic'):
            target.effects.add(PoisonVulnerability(5))
    
    @_action_decorator(cooldown=100, melee=False) #type: ignore
    def blood_ritual(self, party: Party, target: Pawn) -> None:
        '''
        Sacrifice 50% health from your entire Party to summon a shade of death that moves towards the target. Once reached it will infect the targets soul with a crippling DoT that also applies 10 stacks of Expose Weakness, Magic Vulnerability, and Frailty for 5 turns.
        '''
        dmg = 0
        for member in party.members:
            dmg += member.health // 2
            member.health -= member.health // 2

        target.effects.add(ShadeOfDeath(self, target, self.calculate_damage(dmg, target)))


class Wizard(Character):
    def __init__(self, name:str) -> None:
        symbol: str = '🧙'
        role: str='dps'
        position: Union[Point,Tuple[int,int]] = Point(0, 0)
        health_max: int = 80
        gear = ClothArmor()
        super().__init__(name=name, symbol=symbol, role=role, position=position, health_max=health_max, gear=gear)
        self.equip(Wand())

    @_action_decorator(melee=False) #type: ignore
    def magic_missile(self, target: Pawn) -> None:
        '''
        Blast the target with magic missiles! If the target has Magic Vulnerability
        this does 50% additional damage and applies Stun for 1 turn.
        '''
        dmg = self.calculate_damage(20, target)
        if target.effects.vulnerable_to('magic'):
            dmg = self.calculate_damage(100, target)
            target.effects.add(Stun(1))
        target._take_damage(self, dmg, "magic")

    @_action_decorator(cooldown=10, melee=False) #type: ignore
    def fire_bolt(self, target: Pawn) -> None:
        'Blast the target with a ball of Fire and apply 2 stacks of Fire Resistance.'
        target._take_damage(self, self.calculate_damage(50, target), "fire")
        target.effects.add_stacks(FireResistance, stacks=5)

    @_action_decorator(cooldown=10, melee=False) #type: ignore
    def frost_bolt(self, target: Pawn) -> None:
        'Blast the target with a ball of Frost and apply 2 stacks of Frost Resistance.'
        target._take_damage(self, self.calculate_damage(50, target), "frost")
        target.effects.add_stacks(FrostResistance, stacks=5)

    @_action_decorator(cooldown=10, melee=False) #type: ignore
    def teleport(self, target: Pawn, location: Union[Point,Tuple[int,int]]) -> None:
        'Instantly Teleport self or target to anywhere in the arena.'
        target._teleport(location)
        target.face(random.choice(get_adjacent_points(location)))

    @_action_decorator(cooldown=100, melee=False) #type: ignore
    def lightning_strike(self, target: Pawn) -> None:
        '''
        Call down a powerful lightning strike on the target! If the target
        has Magic Vulnerability this deals double damage, applies Stun, and
        5 stacks of Magic Vulnerability on the target for 3 turns.
        '''
        dmg = self.calculate_damage(100, target)
        if target.effects.vulnerable_to('magic'):
            dmg *= 10
            target.effects.add(Stun(3))
            target._take_damage(self, dmg, "magic")
            target.effects.add_stacks(MagicVulnerability, stacks=5)
        else:
            target._take_damage(self, dmg, "magic")


class Bard(Character):
    def __init__(self, name: str) -> None:
        symbol: str = '🎵'
        role: str='dps'
        position: Union[Point,Tuple[int,int]] = Point(0, 0)
        health_max: int = 90
        gear = LeatherArmor()
        super().__init__(name=name, symbol=symbol, role=role, position=position, health_max=health_max, gear=gear)
        self.equip(Lute())

    @_action_decorator(melee=False, affected_by_blind=False) #type: ignore
    def healing_notes(self, party: Party) -> None:
        'All Party members heal for 10% of their health'
        for member in party.members:
            member._heal(member.health//10)

    @_action_decorator(melee=False, affected_by_blind=False) #type: ignore
    def violent_notes(self, party: Party) -> None:
        'All Party members receive 5 stacks of Might'
        for member in party.members:
            member.effects.add_stacks(Might, stacks=5, duration=1)

    @_action_decorator(melee=False, affected_by_blind=False) #type: ignore
    def curative_notes(self, party: Party) -> None:
        'All Party members will receive Cure in 2 turns'
        for member in party.members:
            member.effects.add(CurativeNotes(member))

    @_action_decorator(cooldown=5, melee=False, affected_by_blind=False) #type: ignore
    def magical_notes(self, target: Pawn) -> None:
        '''
        Play a piercing magical note at the enemy that deals Magic damage
        and applies 4 stacks of Expose Weakness. Increased to 6 stacks and
        applies Stun if the target has Magic Vulnerability.
        '''
        dmg = self.calculate_damage(20, target)
        if target.effects.vulnerable_to('magic'):
            target.effects.add(Stun(1))
            target.effects.add_stacks(ExposeWeakness, stacks=6, duration=5)
        else:
            target.effects.add_stacks(ExposeWeakness, stacks=4, duration=5)
        target._take_damage(self, dmg, "magic")

    @_action_decorator(cooldown=100, melee=False, affected_by_blind=False) #type: ignore
    def crescendo(self, party: Party, enemy: Pawn) -> None:
        '''
        Combine all your notes into a chaotic lullaby that triggers all bard
        songs and the Next Attack for all group members will do double damage.
        '''
        # All bard songs + Next Attack buff
        for member in party.members:
            member._heal(member.health//10)
            member.effects.add_stacks(Might, stacks=5, duration=1)
            member.effects.add(CurativeNotes(member))
            member.effects.add(NextAttack(1.0))

        dmg = self.calculate_damage(20, enemy)
        if enemy.effects.vulnerable_to('magic'):
            enemy.effects.add(Stun(1))
            enemy.effects.add_stacks(ExposeWeakness, stacks=6, duration=5)
        else:
            enemy.effects.add_stacks(ExposeWeakness, stacks=4, duration=5)
        enemy._take_damage(self, dmg, "magic")