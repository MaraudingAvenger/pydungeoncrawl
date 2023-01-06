import time
from IPython.display import clear_output

from dungeoncrawl.board import Board
from dungeoncrawl.entities.characters import Party
from dungeoncrawl.bosses import Boss
from dungeoncrawl.entities.pawn import Pawn
from dungeoncrawl.utilities.location import Point

class Level:
    board: Board
    party: Party
    boss: Boss
    turn_count: int

    def __init__(self, board: Board, party: Party, boss: Boss, show_board: bool = True, tick_speed: float = 0.25):
        party_starty = [square
                        for row in board.grid
                        for square in row
                        if square.symbol == '🟢']
        boss_starty = [square for row in board.grid for square in row if square.symbol == '🔴'][0]
        
        for pawn, square in zip(party, party_starty):
            pawn._position = square.position
            pawn.move_history = [square.position]

        boss._position = boss_starty.position
        boss.move_history = [boss_starty.position]
        
        self.board = board
        self.party = party
        self.boss = boss
        self.turn_count = 0
        self.show_board = show_board
        self.tick_speed = tick_speed
        
        # place the pawns
        for pawn in self.party:
            self.board.place(pawn, pawn.position)
        self.board.place(self.boss, self.boss.position)

    def move(self, pawn: Pawn, position: Point):
        if pawn.moved_this_turn:
            result = self.board.place(pawn, position)
            if result != 'success':
                pawn._revert_position(result)

    @property
    def _marquis(self):
        return f"~~~~~~ TURN {self.turn_count:<4}~~~~~~\n{self.party._marquis}\n{'_'*80}\n{self.boss._marquis}"

    def __iter__(self):
        while self.party.is_alive and self.boss.is_alive:

            # check movements
            for player in self.party:
                self.move(player, player.position)
            
            if self.turn_count:
                self.boss._tick()
                self.boss._tick_logic(self.party, self.board)
                self.move(self.boss, self.boss.position)
            

            # send tick to party, boss
            self.party._tick()
            self.board._tick()

            self.turn_count += 1

            if self.show_board:
                clear_output(wait=True)
                print(self)
                time.sleep(self.tick_speed)

            # player turns happen here
            yield self.turn_count
        for player in self.party:
            self.move(player, player.position)
        self.boss._tick()
        self.party._tick()
        self.board._tick()
        
        clear_output(wait=True)
        print(self)
        yield self.turn_count

    def __str__(self):
        return f"{self._marquis}\n{self.board}"

class DummyGame(Level):
    def __init__(self, board: Board, party: Party, boss: Boss, show_board: bool = True, tick_speed: float = 0.25):
        super().__init__(board, party, boss, show_board, tick_speed)