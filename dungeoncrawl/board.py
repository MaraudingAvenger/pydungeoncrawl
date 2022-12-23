from functools import singledispatchmethod

from dungeoncrawl.entities.pawn import Pawn
from dungeoncrawl.utilities.location import Point


class Square:
    def __init__(self, position:Point, symbol:str='⬜', impassable:bool=False, is_burning:bool=False, is_lava:bool=False, damage:int=0, occupant:Pawn|None=None) -> None:
        self.position = position
        self._base_symbol = symbol
        self._symbol = symbol
        self._temp_symbol = ''
        self.impassable = impassable
        self.is_burning = is_burning
        self.is_lava = is_lava
        self.damage = damage
        self.occupant = occupant

    @property
    def symbol(self):
        if self.occupied:
            return self.occupant.symbol # type: ignore
        if self._temp_symbol:
            return self._temp_symbol
        return self._symbol

    def toggle_burning(self, damage:int=3) -> None:
        if self.is_burning:
            self.is_burning = False
            self._symbol = self._base_symbol
            self.damage = 0
        else:
            self.is_burning = True
            self._symbol = '🔥'
            self.damage = damage

    def toggle_lava(self) -> None:
        if self.is_lava:
            self.is_lava = False
            self._symbol = self._base_symbol
            self.damage = 0
        else:
            self.is_lava = True
            self._symbol = '🟥'
            self.damage = 10000

    def set_temp_symbol(self, symbol:str) -> None:
        self._symbol = symbol
    def clear_temp_symbol(self) -> None:
        self._symbol = ''
        
    @property
    def occupied(self) -> bool:
        return self.occupant is not None

    def trigger_effect(self) -> None:
        if self.occupied and (self.is_burning or self.is_lava):
            self.occupant._take_damage(self.damage) # type: ignore

    def place(self, new_occupant:Pawn) -> str:
        '''Place a pawn in the square; returns True if successful.'''
        if self.occupied:
            return "the square is occupied!"    
        if self.impassable:
            return "the square is impassable!"
        self.occupant = new_occupant
        return 'success'

    def __repr__(self):
        return self.symbol if not self.occupied else self.occupant.symbol # type: ignore

    def __str__(self):
        return self.symbol if not self.occupied else self.occupant.symbol # type: ignore


class Board:
    def __init__(self, grid: list[list[Square]]|None = None, grid_size:int=20):  # assume all levels are square
        if grid:
            self.grid_size = len(grid)
            self.grid = []
            for x in range(len(grid)):
                self.grid.append([])
                for y in range(len(grid[x])):
                    self.grid[x].append(grid[y][x])
        else:
            self.grid_size = grid_size
            self.grid = []

            for y in range(grid_size):
                self.grid.append([])
                for x in range(grid_size):
                    self.grid[y].append(Square(Point(x, y)))

    def _tick(self):
        for row in self.grid:
            for square in row:
                if square.occupied and square.position != square.occupant.position:
                    square.occupant = None
                square.trigger_effect()
 
    def at(self, position: Point|tuple[int,int]) -> Square:
        "get square at position (x, y)"
        if isinstance(position, tuple):
            position = Point(position[0], position[1])
        return self.grid[position.y][position.x]

    def players_in_positions(self, *positions: Point|tuple[int,int]) -> list[Pawn|None]:
        "get a list of players in the provided positions"
        return [self.at(pos).occupant for pos in positions if self.at(pos).occupied]
    
    def place(self, pawn: Pawn, position: Point) -> str:
        '''Place a pawn in the square; returns True if successful.'''
        if 0 > position.x >= len(self.grid[0]) or 0 > position.y >= len(self.grid):
            return "the square is out of bounds!"
        return self.at(position).place(pawn)
    
    def __repr__(self):
        return f"Board({len(self.grid)} * {len(self.grid[0])} grid)"

    def __str__(self):
        s = ""
        for y in range(len(self.grid)-1, -1, -1):
            for x in range(len(self.grid[0])):
                s += str(self.grid[y][x].symbol)
            s += "\n"

        return s

    #TODO: need __getitem__?
    #TODO: need __setitem__?

    def __getitem__(self, position: Point) -> Square:
        return self.at(position)


if __name__ == "__main__":
    board = Board()
    print(board)
