
from dungeoncrawl.entities.effects import Effect
from dungeoncrawl.entities.pawn import Pawn


class Square:
    symbol: str
    impassable: bool
    effects: list[Effect]
    occupant: Pawn | None

    def __init__(self, symbol: str = '.', impassable: bool = False, effects: list[Effect] | None = None) -> None:
        self.symbol = symbol
        self.impassable = impassable
        self.effects = effects or []
        self.occupant = None  # TODO: maybe this should be a list?

    @property
    def has_effect(self) -> bool:
        return len(self.effects) > 0

    def place(self, occupant: Pawn) -> bool:
        '''Place a pawn in the square; returns True if successful.'''
        if self.occupant is not None:
            return False
        self.occupant = occupant
        return True

    def __repr__(self) -> str:
        return f"Square({self.symbol}{' '+', '.join(effect.name for effect in self.effects) if self.has_effect else ''})"

    def __str__(self) -> str:
        return f"{self.symbol}"


class Board:
    def __init__(self, grid_size):  # assume all levels are square
        self.grid_size = grid_size
        self.grid = []

        for x in range(grid_size):
            self.grid.append([])
            for y in range(grid_size):
                self.grid[x].append(Square())

    def at(self, x: int, y: int) -> Square:
        "get square at position (x, y)"
        return self.grid[x][y]
