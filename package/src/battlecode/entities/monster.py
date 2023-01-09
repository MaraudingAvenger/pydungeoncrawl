from typing import Tuple, Union
from .effects import Effects
from .pawn import Pawn
from .characters import Party

from ..utilities.location import Point, distance_between


import functools

class Monster(Pawn):
    # type: ignore
    def __init__(self, name: str, position: Union[Point, Tuple[int, int]] = Point(0, 0), health_max: int = 500, symbol: str = '👹'):
        super().__init__(name=name, position=position, health_max=health_max, symbol=symbol)
        self.effects = Effects()
        self.health = self.health_max

    def _get_target(self, party: Party) -> Pawn:
        '''Get the target to attack. Tank -> DPS -> Healer.'''
        if party.tank.is_alive:
            return party.tank
        elif any(member.is_alive for member in party.dps):
            nearest = None
            distance = 9999
            for member in party.dps:
                if distance_between(self.position, member.position) < distance and member.is_alive:
                    nearest = member
                    distance = distance_between(self.position, member.position)
            return nearest # type: ignore
        else:
            return party.healer

        
# vulnerabilities: logic to check effects and double the values if they're in the "vulnerable" category

#TODO: resistances and vulnerabilities

#TODO: telegraph system
#TODO: aggro system! "I'm looking at _____(pawn)"
#     takes a function like a callback to decide?
#     takes a list of pawns?
#     *   checks pawns in a radius around the monster?
#     *   checks pawn health?

