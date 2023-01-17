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