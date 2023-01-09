from dataclasses import dataclass, field
from functools import singledispatchmethod
from typing import Protocol


class Loot(Protocol):
    name: str
    weight: float
    value: int

@dataclass
class Gear:
    name: str = field(init=True, hash=True)
    category: str = field(init=True, hash=True)
    description: str = field(init=True, default="", hash=False)

    damage: int = field(init=True, default=0, hash=False)
    damage_type: str = field(init=True, default="physical", hash=False)
    
    bonus_damage_output_percent: float = field(
        init=True, default=0, hash=False)

    damage_reduction_number: int = field(init=True, default=0, hash=False)
    damage_reduction_percent: float = field(
        init=True, default=0, hash=False)

    bonus_max_health: int = field(init=True, default=0, hash=False)
    bonus_max_health_percent: float = field(init=True, default=0, hash=False)

    def __repr__(self) -> str:
        if self.damage:
            return f"{self.name} ({self.category}, {self.damage} damage)"
        return f"{self.name} ({self.category}, {self.damage_reduction_percent:.0%} protection)"

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

    @property
    def damage_reduction(self) -> int:
        return sum([item.damage_reduction_number for item in self])

    @property
    def damage_reduction_percent(self) -> float:
        return sum([item.damage_reduction_percent for item in self])

    @property
    def bonus_damage_output(self) -> int:
        return sum([item.damage for item in self])
    
    @property
    def bonus_damage_output_percent(self) -> float:
        return sum([item.bonus_damage_output_percent for item in self])
    
    def __iter__(self):
        return iter(self._gear.values())
    def __repr__(self) -> str:
        return f"Equipment({', '.join([str(item) for item in self])})"
    def __str__(self) -> str:
        return f"Equipment({', '.join([str(item) for item in self])})"
    def __getitem__(self, key: str) -> Gear:
        return self._gear[key]
