from dataclasses import dataclass
import random


@dataclass
class Stat:
    name: str
    value: int

    @property
    def modifier(self) -> int:
        return (self.value - 10) // 2

    def reroll(self) -> int:
        score = random.randint(3, 18)
        self.value = score
        return score

    def __repr__(self) -> str:
        return f"{self.name}: {self.value}({self.modifier:+})"

    def __hash__(self) -> int:
        return hash((self.name, self.value, self.modifier))

    def __eq__(self, __o) -> bool:
        if isinstance(__o, Stat):
            return self.name == __o.name and self.value == __o.value
        if isinstance(__o, (int, float)):
            return self.value == __o
        raise TypeError(
            f"Cannot compare{self.__class__.__name__} and {__o.__class__.__name__}"
        )

    def __gt__(self, __o) -> bool:
        if isinstance(__o, Stat):
            return self.value > __o.value
        if isinstance(__o, (int, float)):
            return self.value > __o
        raise TypeError(
            f"Cannot compare{self.__class__.__name__} and {__o.__class__.__name__}"
        )

    def __ge__(self, __o) -> bool:
        if isinstance(__o, Stat):
            return self.value >= __o.value
        if isinstance(__o, (int, float)):
            return self.value >= __o
        raise TypeError(
            f"Cannot compare{self.__class__.__name__} and {__o.__class__.__name__}"
        )

    def __lt__(self, __o) -> bool:
        if isinstance(__o, Stat):
            return self.value < __o.value
        if isinstance(__o, (int, float)):
            return self.value < __o
        raise TypeError(
            f"Cannot compare{self.__class__.__name__} and {__o.__class__.__name__}"
        )

    def __le__(self, __o) -> bool:
        if isinstance(__o, Stat):
            return self.value <= __o.value
        if isinstance(__o, (int, float)):
            return self.value <= __o
        raise TypeError(
            f"Cannot compare{self.__class__.__name__} and {__o.__class__.__name__}"
        )


# TODO: maybe get rid of the Stats class and just use a list of Stat objects instead
class Stats:
    strength: Stat
    dexterity: Stat
    constitution: Stat
    wisdom: Stat
    intelligence: Stat
    charisma: Stat

    def __init__(self) -> None:
        self.reroll_all()

    def reroll_all(self) -> None:
        self.strength = Stat("strength", random.randint(3, 18))
        self.dexterity = Stat("dexterity", random.randint(3, 18))
        self.constitution = Stat("constitution", random.randint(3, 18))
        self.wisdom = Stat("wisdom", random.randint(3, 18))
        self.intelligence = Stat("intelligence", random.randint(3, 18))
        self.charisma = Stat("charisma", random.randint(3, 18))

    def __iter__(self):
        return iter([
            self.strength, self.dexterity, self.constitution, self.wisdom,
            self.intelligence, self.charisma
        ])

    def __repr__(self) -> str:
        return "\n".join(
            str(stat) for stat in [
                self.strength, self.dexterity, self.constitution, self.wisdom,
                self.intelligence, self.charisma
            ])

    def __hash__(self) -> int:
        return hash((stat.__hash__() for stat in self))

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Stats):
            return (self.strength == __o.strength
                    and self.dexterity == __o.dexterity
                    and self.constitution == __o.constitution
                    and self.wisdom == __o.wisdom
                    and self.intelligence == __o.intelligence
                    and self.charisma == __o.charisma)
        raise TypeError(
            f"Cannot compare{self.__class__.__name__} and {__o.__class__.__name__}"
        )
