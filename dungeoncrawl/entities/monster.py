from entities.pawn import Pawn


class Monster(Pawn):
    def __init__(self, name: str, position: tuple[int] = (0, 0)):
        super().__init__(name, position)
