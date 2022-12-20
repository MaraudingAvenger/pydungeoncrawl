from dungeoncrawl.entities.effects import Effects
from dungeoncrawl.entities.pawn import Pawn, Point


class Monster(Pawn):
    # type: ignore
    def __init__(self, name: str, position: Point | tuple[int, int] = Point(0, 0), health_max: int = 500):
        super().__init__(name, position, health_max)
        self.effects = Effects()
        self.health = self.health_max

# vulnerabilities: logic to check effects and double the values if they're in the "vulnerable" category

#TODO: telegraph system

#TODO: resistances and vulnerabilities

#TODO: aggro system! "I'm looking at _____(pawn)"
#     takes a function like a callback to decide?
#     takes a list of pawns?
#     *   checks pawns in a radius around the monster?
#     *   checks pawn health?