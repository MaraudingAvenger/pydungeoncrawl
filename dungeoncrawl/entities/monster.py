from dungeoncrawl.entities.effects import Effects
from dungeoncrawl.entities.pawn import Pawn, Point


import functools

def memoize(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self._history.append(f"{self.__name__} used {func.__name__}({args}, {kwargs})")
        
        return func(*args, **kwargs)
    
    return wrapper

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