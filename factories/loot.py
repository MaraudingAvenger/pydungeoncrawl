from factories.names import NameFactory


class LootFactory:
    def __init__(self) -> None:
        self.names = NameFactory()
        