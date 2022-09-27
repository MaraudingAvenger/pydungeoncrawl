from dungeoncrawl.entities.effects import Effects
from dungeoncrawl.entities.pawn import Pawn, Point
from dungeoncrawl.entities.stats import Stats


class Monster(Pawn):
    # type: ignore
    def __init__(self, name: str, position: Point | tuple[int, int] = Point(0, 0), health_max: int = 100):
        super().__init__(name, position, health_max)
        self.effects = Effects()
        self.stats = Stats()
        self.health = self.health_max
