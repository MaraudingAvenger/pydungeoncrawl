import abc
import heapq

from dungeoncrawl.board import Board
from dungeoncrawl.entities.monster import Monster
from dungeoncrawl.entities.effects import Effect
from dungeoncrawl.entities.pawn import Pawn, _action_decorator
from dungeoncrawl.characters import Party
from dungeoncrawl.utilities.location import Point, distance_between

class Boss(Monster, abc.ABC):
    @abc.abstractmethod
    def _tick_logic(self, party: Party, board: Board):
        ...

    def _astar(self, board: Board, start: Point|tuple, goal: Point|tuple) -> list[Point] | None:

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

                if 0 <= neighbor[0] < len(board.grid[0]):
                    if 0 <= neighbor[1] < len(board.grid):
                        if board.grid[neighbor[1]][neighbor[0]].impassable and neighbor != goal:
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
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + distance_between(neighbor, goal)

                    heapq.heappush(oheap, (fscore[neighbor], neighbor))

class DummyBoss(Boss):
    def __init__(self):
        name="Dummy Boss"
        position=Point(0, 0)
        health_max=10000
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
            self.attack(target)

    @_action_decorator(cooldown=2, melee=True)
    def attack(self, target: Pawn):
        target._take_damage(self, 10, "physical")