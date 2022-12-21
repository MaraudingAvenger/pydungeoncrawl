from dungeoncrawl.board import Board
from dungeoncrawl.entities.monster import Monster
from dungeoncrawl.entities.effects import Effect
from dungeoncrawl.factories.loot import LootFactory

class Controller:
    board: Board
    loot_pool: LootFactory
    turn_count: int
    

    def tick(self):
        # tick players (actions and movement)
        # tick monsters (actions and movement)
        # iterate through all pawns and tick their effects
        self.turn_count += 1
        pass

    def move(self, pawn, position):
        if self.board.place(pawn, position): # board needs to clear the previous cell
            pawn.position = position