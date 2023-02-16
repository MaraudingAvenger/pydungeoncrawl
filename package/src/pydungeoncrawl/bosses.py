import copy
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
            self.telegraph = "is going to attack EVERYONE next turn!"

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

        self.telegraph = f"is going to insult the closest person!"

        self.face(target)
        if not self.is_on_cooldown("make a ruckus"):
            self.make_a_ruckus(party)
        else:
            self.shout_at(target)


class LostKobold(Boss):
    def __init__(self):
        name="Kipper"
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
        name="Lytharra"
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
        name="Shyraki"
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
        name="Vyrliath"
        position=Point(0, 0)
        health_max=20000
        super().__init__(name=name, position=position, health_max=health_max)
        self.equip(Claymore())

        self.last_party_positions : List = [] # #<== Death touch mechanic property

    def get_target(self, party: Party) -> Pawn:
        return self._get_target(party)

    def _tick_logic(self, party: Party, board: Board):
        self.telegraph = None
        target = self._get_target(party)

        if self._turn and self._turn % 5 == 0:
            self.last_party_positions = [p.position for p in party]
            self.telegraph = "is going to devour your souls if you don't move this turn!!!"
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
        self._action_cycle = itertools.cycle([self.decimate, self.roar_of_giants, self.colossal_smash])
        self._furthest_position : Point = Point(0, 0)

    def get_target(self, party: Party) -> Pawn:
        # get closest party member
        return min(party.members, key=lambda p: distance_between(self.position, p.position))

    def _tick_logic(self, party: Party, board: Board):
        self.telegraph = None
        target = self.get_target(party)

        if self._turn and self._turn % 10 == 0:
            self._cycling = True

        if self._throwing:
            self.throw_boulder(self._furthest_position, party)
        
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
                path = list(self._astar(board=board, start=self.position, goal=target.position)) # type: ignore
                if path:
                    self.move_toward(path[0])
        
        self._throwing = random.random() <= 0.1 # 10% chance to throw a boulder
        if self._throwing:
            person = max(party.members, key=lambda player: distance_between(self.position, player.position))
            self._furthest_position = copy.copy(person.position)
            self.telegraph = f"is about to throw a boulder at {person.name}'s position!"

    @_action_decorator(cooldown=10, melee=True) # type: ignore
    def decimate(self, party: Party, **kwargs):
        target = self.get_target(party)
        target._take_damage(self, self.calculate_damage(90, target), "physical") # high dmg due to equipped TreeTrunk
        self._was_in_melee = True
    
    @_action_decorator(cooldown=10, melee=False, affected_by_blind=False) # type: ignore
    def roar_of_giants(self, party: Party, **kwargs):
        for pawn in party:
            pawn.effects.add_stacks(Frailty, stacks=10, duration=3)
    
    @_action_decorator(cooldown=10, melee=False, affected_by_blind=True, affected_by_root=True) # type: ignore
    def colossal_smash(self, party: Party, **kwargs):
        for pawn in party:
            pawn._take_damage(self, self.calculate_damage(60, pawn), "physical")
    
    @_action_decorator(cooldown=10, melee=False, affected_by_blind=True, affected_by_root=False) # type: ignore
    def throw_boulder(self, point: Point, party: Party):
        unlucky = list(filter(lambda target: target.position == point, party.members))
        if unlucky:
            target = unlucky[0]
            target._take_damage(self, self.calculate_damage(150, target), "physical")
            target.effects.add(Stun(duration=2))
    
    @_action_decorator(cooldown=1, melee=False, affected_by_blind=True, affected_by_root=True) # type: ignore
    def death_charge(self, party: Party, board: Board):
        target = self.get_target(party)
        if distance_between(self.position, target.position) > 1.5:
            path = self._astar(board=board, start=self.position, goal=target.position)
            if path is not None:
                self._teleport(path[-2])
        target._take_damage(self, self.calculate_damage(1000, target), "physical")
        self._was_in_melee = True
        self._melee_turn_counter = 0


class ChessMaster(Boss):
    def __init__(self):
        name="Chess Master"
        position=Point(0, 0)
        health_max=200_000
        super().__init__(name=name, position=position, health_max=health_max)

        self._turn_counter = 0
        self._action_cycle = itertools.cycle([self.king, self.queen, self.rook, self.bishop, self.knight, self.curtain])
        self._action_name_cycle = itertools.cycle(["king", "queen", "rook", "bishop", "knight", "pawn advance"])
        self._turn_counter = 0

    def get_target(self, party: Party) -> Pawn:
        # get random party member
        return random.choice(party.members)

    def _tick_logic(self, party: Party, board: Board):
        if self.telegraph:
            next(self._action_cycle)(party, board)
            self.telegraph=None

        if self._turn and self._turn % 5 == 0:
            self._target = self.get_target(party)
            self._attack_position = copy.copy(self._target.position)
            action = next(self._action_name_cycle)
            if action != 'pawn advance':
                self.telegraph = f"is going to use a {action} attack on {self._target.name}!"
            else:
                self.telegraph = f"is going to advance the pawn row!"

        if self._turn_counter:
            self.curtain(party, board)  

    @_action_decorator(cooldown=1, melee=False, affected_by_blind=False, affected_by_root=False) # type: ignore
    def king(self, party: Party, board: Board):
        for xmod in (-1, 0, 1):
            for ymod in (-1, 0, 1):
                if xmod == 0 and ymod == 0:
                    continue
                x = self._attack_position.x + xmod
                y = self._attack_position.y + ymod
                if x < 0 or x >= board.width or y < 0 or y >= board.height:
                    continue
                for member in party.members:
                    if member.position == Point(x, y):
                        member._take_damage(self, self.calculate_damage(160, member), "physical")
    
    @_action_decorator(cooldown=1, melee=False, affected_by_blind=False, affected_by_root=False) # type: ignore
    def queen(self, party: Party, board: Board):
        moves = self._queen_moves(board, self._attack_position.x, self._attack_position.y)
        for x, y in moves:
            for member in party.members:
                if member.position == Point(x, y):
                    member._take_damage(self, self.calculate_damage(160, member), "physical")

    @_action_decorator(cooldown=1, melee=False, affected_by_blind=False, affected_by_root=False) # type: ignore
    def rook(self, party: Party, board: Board):
        moves = self._rook_moves(board, self._attack_position.x, self._attack_position.y)
        for x, y in moves:
            for member in party.members:
                if member.position == Point(x, y):
                    member._take_damage(self, self.calculate_damage(160, member), "physical")

    @_action_decorator(cooldown=1, melee=False, affected_by_blind=False, affected_by_root=False) # type: ignore
    def bishop(self, party: Party, board: Board):
        moves = self._bishop_moves(board, self._attack_position.x, self._attack_position.y)
        for x, y in moves:
            for member in party.members:
                if member.position == Point(x, y):
                    member._take_damage(self, self.calculate_damage(160, member), "physical")

    @_action_decorator(cooldown=1, melee=False, affected_by_blind=False, affected_by_root=False) # type: ignore
    def knight(self, party: Party, board: Board):
        moves = self._knight_moves(board, self._attack_position.x, self._attack_position.y)
        for x, y in moves:
            for member in party.members:
                if member.position == Point(x, y):
                    member._take_damage(self, self.calculate_damage(160, member), "physical")

    def _bishop_moves(self, board: Board, x: int, y: int) -> set[tuple[int,int]]:
        moves = set()
        for i in range(1, board.width):
            if x + i <= board.width and y + i <= board.width:
                moves.add((x+i, y+i))
            if x + i <= board.width and y - i >= 0:
                moves.add((x+i, y-i))
            if x - i >= 0 and y + i <= board.width:
                moves.add((x-i, y+i))
            if x - i >= 0 and y - i >= 0:
                moves.add((x-i, y-i))
        return moves

    def _queen_moves(self, board: Board, x: int, y: int) -> set[tuple[int,int]]:
        moves = set()
        
        # Horizontal and vertical moves
        for i in range(board.width):
            if i != x:
                moves.add((i, y))
            if i != y:
                moves.add((x, i))
        
        # Diagonal moves
        moves = moves.union(self._bishop_moves(board, x, y))
        
        return moves

    def _rook_moves(self, board: Board, x: int, y: int) -> set[tuple[int,int]]:
        moves = set()
        
        # Horizontal and vertical moves
        for i in range(board.width):
            if i != x:
                moves.add((i, y))
            if i != y:
                moves.add((x, i))
        
        return moves

    def _knight_moves(self, board: Board, x: int, y: int) -> set[tuple[int,int]]:
        moves = set()
        possible_moves = [(x+2, y+1), (x+2, y-1), (x-2, y+1), (x-2, y-1), (x+1, y+2), (x+1, y-2), (x-1, y+2), (x-1, y-2)]
        for i, j in possible_moves:
            if 0 <= i <= board.width-1 and 0 <= j <= board.height-1:
                moves.add((i, j))
        return moves
    
    @_action_decorator(cooldown=1, melee=False, affected_by_blind=False, affected_by_root=False) # type: ignore
    def curtain(self, _party: Party, board: Board):
        adding_lava = True
        if self._turn_counter >= board.width // 3:
            adding_lava = False

        # top
        if self._turn_counter > 0:
            prev = self._turn_counter - 1
            for square in board.grid[prev]:
                square.toggle_lava()
        if adding_lava:
            for square in board.grid[self._turn_counter]:
                square.toggle_lava()

        # bottom
        if self._turn_counter > 0:
            prev = len(board.grid) - self._turn_counter
            for square in board.grid[prev]:
                square.toggle_lava()
        if adding_lava:
            for square in board.grid[len(board.grid) - self._turn_counter - 1]:
                square.toggle_lava()

        if adding_lava:
            self._turn_counter += 1
        else:
            self._turn_counter = 0