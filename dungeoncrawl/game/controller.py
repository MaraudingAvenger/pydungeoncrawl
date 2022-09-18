from board.grid import Board
from dungeoncrawl.entities.monster import Monster
from dungeoncrawl.entities.effects import Effect
from dungeoncrawl.factories.loot import LootFactory

class Controller:
    board: Board
    loot_pool: LootFactory
    