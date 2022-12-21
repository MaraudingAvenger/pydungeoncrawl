from dungeoncrawl.entities.monster import Monster
from dungeoncrawl.entities.effects import Effect
from dungeoncrawl.entities.pawn import Pawn
from dungeoncrawl.characters import Party
from dungeoncrawl.utilities.location import distance_between

class DummyBoss(Monster):
    def __init__(self, name="Dummy Boss", position=(0, 0), health_max=1000):
        super().__init__(name, position, health_max)
        self._symbol = '😈'

    def tick(self, party: Party):
        tank = party.tank

        if distance_between(self.position, tank.position) > 1.5:
            self.move_towards(tank.position)
        else:
            self.attack(tank)

    def attack(self, target: Pawn):
        target._take_damage(10)
        target.effects.add(Effect(name="Dummy Boss Attack", duration=5, heal_over_time=2))
