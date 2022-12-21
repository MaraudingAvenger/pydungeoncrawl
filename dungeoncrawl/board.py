from functools import singledispatchmethod

from dungeoncrawl.entities.pawn import Pawn
from dungeoncrawl.utilities.location import Point


class Square:
    def __init__(self, position:Point, symbol:str='⬜', impassable:bool=False, is_burning:bool=False, is_lava:bool=False, damage:int=0, occupant:Pawn|None=None) -> None:
        self.position = position
        self._base_symbol = symbol
        self._symbol = symbol
        self.impassable = impassable
        self.is_burning = is_burning
        self.is_lava = is_lava
        self.damage = damage
        self.occupant = occupant

    @property
    def symbol(self):
        if self.occupied:
            return self.occupant._symbol # type: ignore
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

    @property
    def occupied(self) -> bool:
        return self.occupant is not None

    def place(self, new_occupant:Pawn) -> bool:
        '''Place a pawn in the square; returns True if successful.'''
        if self.occupied or self.impassable:
            return False
        self.occupant = new_occupant
        return True

    def __repr__(self):
        return self.symbol

    def __str__(self):
        return self.symbol


class Board:
    def __init__(self, grid: list[list[dict]]|None = None, grid_size:int=20):  # assume all levels are square
        if grid:
            self.grid_size = len(grid)
            self.grid = []
            for x in range(len(grid)):
                self.grid.append([])
                for y in range(len(grid[x])):
                    self.grid[x].append(Square(Point(x, y), **grid[x][y]))
        else:
            self.grid_size = grid_size
            self.grid = []

            for x in range(grid_size):
                self.grid.append([])
                for y in range(grid_size):
                    self.grid[x].append(Square(Point(x, y)))

    @singledispatchmethod
    def at(self, x: int, y: int) -> Square:
        "get square at position (x, y)"
        return self.grid[x][y]

    @at.register
    def _(self, position: Point) -> Square:
        "get square at position (x, y)"
        return self.grid[position.x][position.y]

    @singledispatchmethod
    def place(self, pawn: Pawn, position: Point) -> bool:
        '''Place a pawn in the square; returns True if successful.'''
        return self.at(position).place(pawn)

    @place.register
    def _(self, pawn: Pawn, x: int, y: int) -> bool:
        '''Place a pawn in the square; returns True if successful.'''
        return self.at(x, y).place(pawn)

    def __repr__(self):
        return f"Board({len(self.grid)} * {len(self.grid[0])} grid)"

    def __str__(self):
        return "\n".join("".join(str(square) for square in row) for row in self.grid)

    #TODO: need __getitem__?
    #TODO: need __setitem__?


if __name__ == "__main__":
    board = Board()
    print(board)
