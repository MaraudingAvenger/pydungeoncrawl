from .things import Equipment
from .stats import Stats
from .body import Body

class Character:
    name: str
    stats: Stats
    body: Body
    inventory: list[Equipment]
    money: int

    def __init__(self, name: str) -> None:
        self.name = name
        self.stats = Stats()
        self.body = Body(10)
        self.inventory = []
        self.money = 0

    def equip(self, equipment:Equipment) -> None:
        self.body.equip(equipment)

    def __repr__(self) -> str:
        return f"{self.name}\n\nStats:\n{self.stats}\n\nStatus:\n{self.body}\n\nGear:\n{self.inventory}"

    def __str__(self) -> str:
        return self.name

    @property
    def character_sheet(self) -> str:
        return self.__repr__()


if __name__ == "__main__":
    character = Character("Jimmy McNuggets")

    print("stats:")
    print(character.stats)
    i = character.stats.strength.reroll()
    print(i)
    print("\nnew stats:")
    print(character.stats)
