from board.grid import Board
from entities.monster import Monster
from entities.effects import Effect
from factories.loot import LootFactory

class Controller:
    board: Board
    loot_pool: LootFactory
    