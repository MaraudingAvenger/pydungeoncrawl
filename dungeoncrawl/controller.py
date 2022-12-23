from dungeoncrawl.board import Board
from dungeoncrawl.characters import Party
from dungeoncrawl.bosses import Boss
from dungeoncrawl.entities.pawn import Pawn
from dungeoncrawl.utilities.location import Point

class Game:
    board: Board
    party: Party
    boss: Boss
    turn_count: int

    def __init__(self, board: Board, party: Party, boss: Boss):
        self.board = board
        self.party = party
        self.boss = boss
        self.turn_count = 0
        
        # place the pawns
        for pawn in self.party:
            self.board.place(pawn, pawn.position)
        self.board.place(self.boss, self.boss.position)

    def move(self, pawn: Pawn, position: Point|tuple[int,int]):
        if pawn.moved_this_turn:
            result = self.board.place(pawn, position)
            if result != 'success':
                pawn._revert_position(result)

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

            # display the board
            print(self.board)

            # player turns happen here
            yield self.turn_count
        for player in self.party:
            self.move(player, player.position)
        self.boss._tick()
        self.party._tick()
        self.board._tick()
        print(self.board)
        yield self.turn_count

