from effects import Effect


class Square:
    x: int
    y: int
    symbol: str
    impassable: bool
    effects: list[Effect]

    def __init__(self, x:int, y:int, symbol:str = '.') -> None:
        self.x = x
        self.y = y
        self.symbol = symbol
        self.impassable = False
        self.effects = []

    @property
    def position(self) -> tuple[int,int]:
        return (self.x, self.y)

    @property
    def has_effect(self) -> bool:
        return len(self.effects) > 0

    def __repr__(self) -> str:
        return f"Square({self.x}, {self.y}, {self.symbol})"

    def __str__(self) -> str:
        return f"{self.symbol}"


class Grid:
    def __init__(self, n): # assume all levels are square
        self.n = n
        self.grid = []

        for x in range(n):
            self.grid.append([])
            for y in range(n):
                self.grid[x].append(Square(x, y))
        
    def at(self, x:int, y:int) -> Square:
        return self.grid[x][y]


