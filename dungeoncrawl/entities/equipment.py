from dataclasses import dataclass, field
from functools import singledispatchmethod
from typing import Protocol


class Loot(Protocol):
    name: str
    weight: float
    value: int

@dataclass
class Gear:
    name: str = field(init=True, repr=True, hash=True)
    category: str = field(init=True, repr=True, hash=True)
    description: str = field(init=True, default="", repr=True, hash=False)

    damage: int = field(init=True, default=0, hash=False)
    bonus_damage_output_percent: float = field(
        init=True, default=0, hash=False)

    bonus_damage_received: int = field(init=True, default=0, hash=False)
    bonus_damage_received_percent: float = field(
        init=True, default=0, hash=False)

    bonus_max_health: int = field(init=True, default=0, hash=False)
    bonus_max_health_percent: float = field(init=True, default=0, hash=False)


class Empty(Gear):
    def __init__(self, category) -> None:
        super().__init__(
            name="Empty",
            category=category,
            description="An empty slot.",
        )

@dataclass
class GearSet:
    name: str = field(init=True, repr=True, hash=True)
    description: str = field(init=True, default="", repr=True, hash=False)
    gear: list[Gear] = field(init=True, default_factory=list, hash=False)

    def __iter__(self):
        return iter(self.gear)

class Equipment:
    def __init__(self, *gear: Gear) -> None:
        self._gear: dict[str, Gear] = {
            "head": Empty("head"),
            "chest": Empty("chest"),
            "legs": Empty("legs"),
            "feet": Empty("feet"),
            "hands": Empty("hands"),
            "weapon": Empty("weapon"),
            "offhand": Empty("offhand"),
        }

        for item in gear:
            self._gear[item.category] = item

    @singledispatchmethod
    def equip(self, item: Gear) -> None:
        self._gear[item.category] = item
    @equip.register
    def _(self, location:str, item: Gear) -> None:
        self._gear[location] = item
    @equip.register
    def _(self, gear_set: GearSet) -> None:
        for item in gear_set:
            self.equip(item)

    @singledispatchmethod
    def unequip(self, item: Gear) -> None:
        self._gear[item.category] = Empty(item.category)
    @unequip.register
    def _(self, location: str) -> None:
        self._gear[location] = Empty(location)
    @unequip.register
    def _(self, gear_set: GearSet) -> None:
        for item in gear_set:
            self.unequip(item)

    def __getitem__(self, key: str) -> Gear:
        return self._gear[key]
