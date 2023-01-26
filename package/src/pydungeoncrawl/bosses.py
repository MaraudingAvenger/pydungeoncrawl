import abc
import heapq
import itertools
import random
from typing import List, Tuple, Union

from .entities.board import Board
from .entities.monster import Monster
from .entities.pawn import Pawn, _action_decorator
from .entities.characters import Party

from .utilities.location import Point, distance_between, bresenham

from .debuffs import Curse, Embarrassed, Frailty, Stun
from .buffs import HoT
from .weapons import Claymore, Dagger, Sword, TreeTrunk

class Boss(Monster, abc.ABC):
    @abc.abstractmethod
    def _tick_logic(self, party: Party, board: Board):
        ...

    def _astar(self, board: Board, start: Union[Point,Tuple], goal: Union[Point,Tuple]) -> list[Point] | None:

        start = tuple(start)
        goal = tuple(goal)

        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0),
                    (1, 1), (1, -1), (-1, 1), (-1, -1)]
        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: distance_between(start, goal)}

        oheap = []
        heapq.heappush(oheap, (fscore[start], start))
        while oheap:
            current = heapq.heappop(oheap)[1]
            if current == goal:
                data = []
                while current in came_from:
                    data.append(Point(*current))
                    current = came_from[current]
                return data[::-1]

            close_set.add(current)

            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                tentative_g_score = gscore[current] + distance_between(current, neighbor)

                if 0 <= neighbor[0] < board.grid_size:
                    if 0 <= neighbor[1] < board.grid_size:
                        if (board.at(neighbor).impassable or board.at(neighbor).is_lava) and neighbor != goal: # type: ignore
                            continue

                    else:
                        # grid bound y walls
                        continue

                else:
                    # grid bound x walls
                    continue

                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score # type: ignore
                    fscore[neighbor] = tentative_g_score + distance_between(neighbor, goal)

                    heapq.heappush(oheap, (fscore[neighbor], neighbor))



###################
# ~~ TEST BOSS ~~ #
###################

class Golem(Boss):
    '''
    The Golem is a high-damage, implacable foe. It has a large health pool,
    and will steadily attack the party until it is defeated.
    '''
    def __init__(self):
        name="Thunk"
        position=Point(0, 0)
        health_max=20000
        super().__init__(name=name, position=position, health_max=health_max)

    def get_target(self, party: Party) -> Pawn:
        return self._get_target(party)

    def _tick_logic(self, party: Party, board: Board):
        target = self.get_target(party)

        # Telegraphing
        if self._ability_cooldowns.get('Aoe', 0) == 1:
            self.telegraph = "I'm going to attack EVERYONE next turn!"

        # Combat logic
        if distance_between(self.position, target.position) > 1.5:
            path = self._astar(board=board, start=self.position, goal=target.position)
            if path is not None:
                self.move(path[0])
        else:
            if self.is_on_cooldown("aoe"):
                self.attack(target)
            else:
                self.aoe(party)

    @_action_decorator(cooldown=2, melee=True) # type: ignore
    def attack(self, target: Pawn):
        target._take_damage(self, 20, "physical")

    @_action_decorator(cooldown=10) # type: ignore
    def aoe(self, party: Party):
        for pawn in party.members:
            pawn._take_damage(self, 50, "physical")


##################################
# ~~ Training Scenario Bosses ~~ #
##################################

# ~~ First Scenario Boss ~~ #

class TrainingDummy(Boss):
    def __init__(self):
        name="Training Dummy"
        position=Point(0, 0)
        health_max=10000
        super().__init__(name=name, position=position, health_max=health_max)

    def get_target(self, party: Party) -> Pawn:
        return party.closest_to(self)

    @_action_decorator(cooldown=2, melee=False, affected_by_blind=False) # type: ignore
    def shout_at(self, target: Pawn):
        target._add_effect(Embarrassed())

    @_action_decorator(cooldown=3, melee=False, affected_by_blind=False) # type: ignore
    def make_a_ruckus(self, party: Party):
        for pawn in party.members:
            pawn._add_effect(Embarrassed())

    def _tick_logic(self, party: Party, board: Board):
        target = self.get_target(party)

        self.telegraph = f"I'm going to insult the closest person!"

        self.face(target)
        if not self.is_on_cooldown("make a ruckus"):
            self.make_a_ruckus(party)
        else:
            self.shout_at(target)


class LostKobold(Boss):
    def __init__(self):
        name="Lost Kobold"
        position=Point(0, 0)
        health_max=5000
        super().__init__(name=name, position=position, health_max=health_max)
        self.equip(Dagger())

    def get_target(self, party: Party) -> Pawn:
        return self._get_target(party)

    def _tick_logic(self, party: Party, board: Board):
        target = self._get_target(party)

        if distance_between(self.position, target.position) > 1.5:
            path = self._astar(board=board, start=self.position, goal=target.position)
            if path is not None:
                self.move(path[0])
        else:
            self.fumbling_attack(target)

    @_action_decorator(melee=True) # type: ignore
    def fumbling_attack(self, target: Pawn):
        target._take_damage(self, self.calculate_damage(5, target), "physical")


class KoboldMother(Boss):
    def __init__(self):
        name="Kobold Mother"
        position=Point(0, 0)
        health_max=10000
        super().__init__(name=name, position=position, health_max=health_max)
        self.equip(Sword())

    def get_target(self, party: Party) -> Pawn:
        return self._get_target(party)

    def _tick_logic(self, party: Party, board: Board):
        target = self._get_target(party)

        if distance_between(self.position, target.position) > 1.5:
            path = self._astar(board=board, start=self.position, goal=target.position)
            if path is not None:
                self.move(path[0])
        else:
            self.motherly_love(target)

    @_action_decorator(melee=True) # type: ignore
    def motherly_love(self, target: Pawn):
        target._take_damage(self, self.calculate_damage(40, target), "physical")


class KoboldQueen(Boss):
    def __init__(self):
        name="Kobold Queen"
        position=Point(0, 0)
        health_max=20000
        super().__init__(name=name, position=position, health_max=health_max)
        self.equip(Sword())

    def get_target(self, party: Party) -> Pawn:
        return self._get_target(party)

    def _tick_logic(self, party: Party, board: Board):
        target = self._get_target(party)

        if distance_between(self.position, target.position) > 1.5:
            path = self._astar(board=board, start=self.position, goal=target.position)
            if path is not None:
                self.move(path[0])
        else:
            if not self.is_on_cooldown("Curse"):
                self.curse(party)
            else:
                self.savage_strike(target)

    @_action_decorator(melee=True) # type: ignore
    def savage_strike(self, target: Pawn):
        target._take_damage(self, 60, "physical")

    @_action_decorator(cooldown=10) # type: ignore
    def curse(self, party: Party):
        for pawn in list(party.dps) + [party.healer]:
            pawn.effects.add(Curse(caster=self, target=pawn, duration=8, dot_amount=self.calculate_damage(3, pawn)))

class KoboldGoddess(Boss):
    def __init__(self):
        name="Kobold Goddess"
        position=Point(0, 0)
        health_max=20000
        super().__init__(name=name, position=position, health_max=health_max)
        self.equip(Claymore())

        self.last_party_positions : List = [] # #<== Death touch mechanic property

    def get_target(self, party: Party) -> Pawn:
        return self._get_target(party)

    def _tick_logic(self, party: Party, board: Board):
        target = self._get_target(party)

        if self._turn and self._turn % 5 == 0:
            self.last_party_positions = [p.position for p in party]
            self.telegraph = "I'm going to devour your souls if you don't move next turn!!!"
        elif self.telegraph:
            self.devour_souls(party)
        elif distance_between(self.position, target.position) > 1.5:
            path = self._astar(board=board, start=self.position, goal=target.position)
            if path is not None:
                self.move(path[0])
        else:
            if not self.is_on_cooldown("Curse"):
                self.curse(party)
            else:
                self.savage_strike(target)

    @_action_decorator(affected_by_blind=False) # type: ignore
    def devour_souls(self, party: Party):
        for p in party:
            if p.position in self.last_party_positions:
                p._take_damage(self, 666, "physical")
        self.telegraph = None

    @_action_decorator(melee=True) # type: ignore
    def savage_strike(self, target: Pawn):
        target._take_damage(self, 60, "physical")

    @_action_decorator(cooldown=10) # type: ignore
    def curse(self, party: Party):
        for pawn in list(party.dps) + [party.healer]:
            pawn.effects.add(Curse(caster=self, target=pawn, duration=8, dot_amount=self.calculate_damage(3, pawn)))


# 
# Savage Mountain Troll

# Core Mechanic: Regenerates Health
# Attack: Normal heavy attack against melee target.
# cycle:
    # Mechanic 1: Every 10 turns will attack with extreme damage that applies Stun to the target for 2 turns.
    # Mechanic 2: (Follows Mechanic 1) Let's out a roar that applies 10 stacks of Frailty to Party for 3 turns
    # Mechanic 3: (Follows Mechanic 2) Jumps into the air and smashes down causing heavy damage to entire Party.
# random
    # Mechanic 4: (Telegraphed) Throws a giant rock randomly at furthest target. Anyone at that position will receive massive damage and applies Stun for 2 turns.
# Mechanic 5: Death charges the closest target dealing extreme damage if no target is in melee range for 2 turns (can only occur after turn 13) 

class SavageMountainTroll(Boss):
    def __init__(self):
        name="Morgoth Trollkin"
        position=Point(0, 0)
        health_max=20000
        super().__init__(name=name, position=position, health_max=health_max)
        
        self.equip(TreeTrunk())
        self._add_effect(HoT(name="Trollkin Regeneration", duration=float('inf'), heal_amount=5))

        self._throwing = False
        self._was_in_melee = False
        self._melee_turn_counter = 0
        self._cycle_turn_counter = 0
        self._cycling = False
        self._action_cycle = itertools.cycle([self.crushing_attack, self.thunderous_roar, self.stomp])
        self._last_party_positions : List[Point] = [] 

    def get_target(self, party: Party) -> Pawn:
        # get closest party member
        return min(party.members, key=lambda p: distance_between(self.position, p.position))

    def _tick_logic(self, party: Party, board: Board):
        target = self.get_target(party)

        if self._turn and self._turn % 10 == 0:
            self._cycling = True

        if self._throwing:
            self.boulder(
                max(self._last_party_positions, key=lambda p: distance_between(self.position, p)),
                board)
        
        if self._was_in_melee and distance_between(self.position, target.position) > 1.5:
            self._melee_turn_counter += 1

        if not self.acted_this_turn:
            if self._melee_turn_counter >= 2:
                self.death_charge(party=party, board=board)

            elif self._cycling:
                if self._cycle_turn_counter >= 3:
                    self._cycle_turn_counter = 0
                    self._cycling = False
                else:
                    self._cycle_turn_counter += 1
                    next(self._action_cycle)(party, target=target)
            else:
                self.move_toward(target)
        
        self._throwing = random.random() <= 0.1 # 10% chance to throw a boulder
        if self._throwing:
            self._last_party_positions = [p.position for p in party]
            self.telegraph = "The savage mountain troll is about to throw a boulder at the furthest party member's position!"


        

    @_action_decorator(cooldown=10, melee=True) # type: ignore
    def crushing_attack(self, party: Party, **kwargs):
        target = self.get_target(party)
        target._take_damage(self, self.calculate_damage(50, target), "physical") # high dmg due to equipped TreeTrunk
        self._was_in_melee = True
    
    @_action_decorator(cooldown=10, melee=False, affected_by_blind=False) # type: ignore
    def thunderous_roar(self, party: Party, **kwargs):
        for pawn in party:
            pawn.effects.add_stacks(Frailty, stacks=10, duration=3)
    
    @_action_decorator(cooldown=10, melee=False, affected_by_blind=True, affected_by_root=True) # type: ignore
    def stomp(self, party: Party, **kwargs):
        for pawn in list(party.dps) + [party.healer]:
            pawn._take_damage(self, self.calculate_damage(40, pawn), "physical")
    
    @_action_decorator(cooldown=10, melee=False, affected_by_blind=True, affected_by_root=False) # type: ignore
    def boulder(self, point: Point, board: Board,):
        target = board.at(point)
        if target and target.occupant:
            target.occupant._take_damage(self, self.calculate_damage(40, target.occupant), "physical")
            target.occupant.effects.add(Stun(duration=2))
    
    @_action_decorator(cooldown=1, melee=False, affected_by_blind=True, affected_by_root=True) # type: ignore
    def death_charge(self, party: Party, board: Board):
        target = self.get_target(party)
        if distance_between(self.position, target.position) > 1.5:
            path = self._astar(board=board, start=self.position, goal=target.position)
            if path is not None:
                self._teleport(path[-2])
        target._take_damage(self, self.calculate_damage(100, target), "physical")
        self._was_in_melee = True
        self._melee_turn_counter = 0