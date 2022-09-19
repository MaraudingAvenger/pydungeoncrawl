from dungeoncrawl.entities.effects import Effects
from dungeoncrawl.entities.pawn import Pawn
from dungeoncrawl.entities.stats import Stats


class Monster(Pawn):
    def __init__(self, name: str, position: tuple[int] = (0, 0), **kwargs): # type: ignore
        self.name = name
        self.position = position
        self.effects = Effects()
        self.stats = Stats()
        self.health_max = kwargs.get('health_max', 100)
        self.health = self.health_max

    

