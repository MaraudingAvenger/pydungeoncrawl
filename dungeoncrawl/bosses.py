import abc

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


class DummyBoss(Boss):
    def __init__(self):
        name="Dummy Boss"
        position=Point(0, 0)
        health_max=10000
        super().__init__(name=name, position=position, health_max=health_max)

    def _tick_logic(self, party: Party, board: Board):
        tank = party.tank

        if distance_between(self.position, tank.position) > 1.5:
            self.move_toward(tank.position)
        else:
            self.attack(tank)

    @_action_decorator(cooldown=2, melee=True)
    def attack(self, target: Pawn):
        target._take_damage(10)
        target.effects.add(Effect(name="Dummy Boss Attack", duration=5, heal_over_time=2))
