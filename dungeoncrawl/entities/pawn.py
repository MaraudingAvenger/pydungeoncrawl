from dungeoncrawl.entities.effects import Effect
from dungeoncrawl.entities.stats import Stats


# TODO: consider making this an abstract base class
class Pawn:
    name: str
    position: tuple[int]
    effects: list[Effect]
    stats: Stats

    # TODO: needs to be filled out
    def __init__(self, name: str, position: tuple[int]) -> None:
        self.name = name
        self.position = position

    @property
    def has_effects(self) -> bool:
        return len(self.effects) > 0

    # TODO: needs to be filled out
    def move(self, x: int, y: int) -> None:
        pass
