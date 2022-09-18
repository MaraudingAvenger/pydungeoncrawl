from board.grid import Board
from entities.monster import Monster
from entities.effects import Effect
from entities.items import LootGenerator

class Controller:
    board: Board
    loot_pool: LootGenerator
    