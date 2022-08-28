from game.effects import Effect


class Square:
    symbol: str
    impassable: bool
    effects: list[Effect]

    def __init__(self, symbol: str = '.', impassable: bool = False, effects: list[Effect] | None = None) -> None:
        self.symbol = symbol
        self.impassable = impassable
        self.effects = effects or []

    @property
    def has_effect(self) -> bool:
        return len(self.effects) > 0

    def __repr__(self) -> str:
        return f"Square({self.symbol}{' '+', '.join(effect.name for effect in self.effects) if self.has_effect else ''})"

    def __str__(self) -> str:
        return f"{self.symbol}"


class Grid:
    def __init__(self, n):  # assume all levels are square
        self.n = n
        self._grid = []

        for x in range(n):
            self._grid.append([])
            for y in range(n):
                self._grid[x].append(Square())

    def at(self, x: int, y: int) -> Square:
        return self._grid[x][y]
