from dungeoncrawl.entities.pawn import Pawn


class Monster(Pawn):
    def __init__(self, name: str, position: tuple[int] = (0, 0)): # type: ignore
        super().__init__(name, position)
