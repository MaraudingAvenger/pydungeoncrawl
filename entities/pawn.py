from entities.effects import Effect
from entities.stats import Stats


class Pawn:
    effects: list[Effect]
    stats: Stats

    @property
    def has_effects(self) -> bool:
        return len(self.effects) > 0
