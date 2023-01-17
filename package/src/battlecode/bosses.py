import abc
import heapq
from typing import Tuple, Union

from .entities.board import Board
from .entities.monster import Monster
from .entities.pawn import Pawn, _action_decorator
from .entities.characters import Party

from .utilities.location import Point, distance_between, bresenham

from .debuffs import Curse, Embarrassed
from .weapons import Dagger, Sword

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
    def __init__(self):
        name="Thunk"
        position=Point(0, 0)
        health_max=20000
        super().__init__(name=name, position=position, health_max=health_max)

    def get_target(self, party: Party) -> Pawn:
        return self._get_target(party)

    def _tick_logic(self, party: Party, board: Board):
        target = self._get_target(party)

        if distance_between(self.position, target.position) > 1.5:
            path = self._astar(board=board, start=self.position, goal=target.position)
            if path is not None:
                self.move(path[0])
        else:
            if self.is_on_cooldown("Attack"):
                self.aoe(party)
            else:
                self.attack(target)

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