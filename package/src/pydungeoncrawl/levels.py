from .entities.board import Board
from .entities.characters import Party
from .bosses import Boss, TrainingDummy
from ._level import Level
from .utilities.map_making import get_map


class BlankLevel(Level):
    def __init__(self, party: Party, boss: Boss, board: Board, show_board: bool=True, tick_speed: float=0.25) -> None:
        super().__init__(board=board, party=party, boss=boss, show_board=show_board, tick_speed=tick_speed)

class MovementTraining(Level):
    def __init__(self, party: Party, boss:Boss, show_board: bool=True, tick_speed: float=0.25) -> None:
        board = get_map('simple_map.json')
        super().__init__(board=board, party=party, boss=boss, show_board=show_board, tick_speed=tick_speed)

class ForestPath(Level):
    def __init__(self, party: Party, boss:Boss, show_board: bool=True, tick_speed: float=0.25) -> None:
        board = get_map('forest_path.json')
        super().__init__(board=board, party=party, boss=boss, show_board=show_board, tick_speed=tick_speed)
        
class RiverFord(Level):
    def __init__(self, party: Party, boss:Boss, show_board: bool=True, tick_speed: float=0.25) -> None:
        board = get_map('river_ford.json')
        super().__init__(board=board, party=party, boss=boss, show_board=show_board, tick_speed=tick_speed)

class BeachParty(Level):
    def __init__(self, party: Party, boss:Boss, show_board: bool=True, tick_speed: float=0.25) -> None:
        board = get_map('beach_party.json')
        super().__init__(board=board, party=party, boss=boss, show_board=show_board, tick_speed=tick_speed)

class CabinAtTheLake(Level):
    def __init__(self, party: Party, boss:Boss, show_board: bool=True, tick_speed: float=0.25) -> None:
        board = get_map('cabin_at_the_lake.json')
        super().__init__(board=board, party=party, boss=boss, show_board=show_board, tick_speed=tick_speed)

class HigherGround(Level):
    def __init__(self, party: Party, boss:Boss, show_board: bool=True, tick_speed: float=0.25) -> None:
        board = get_map('higher_ground.json')
        super().__init__(board=board, party=party, boss=boss, show_board=show_board, tick_speed=tick_speed)

class LavaCave(Level):
    def __init__(self, party: Party, boss:Boss, show_board: bool=True, tick_speed: float=0.25) -> None:
        board = get_map('lava_cave.json')
        super().__init__(board=board, party=party, boss=boss, show_board=show_board, tick_speed=tick_speed)