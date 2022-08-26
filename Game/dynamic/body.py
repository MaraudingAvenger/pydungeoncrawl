import copy

from .things import Equipment, Wearable
from .weapons import Weapon
from .weapons import Fist

class BodyPart:
    _hp: int
    name: str
    weapon_equipment: Equipment|None
    armor_equipment: Equipment|None

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value) -> None:
        if value < 0:
            self._hp = 0
        else:
            self._hp = value

    def __init__(self, name: str, hp: int = 0) -> None:
        self.name = name
        self.hp = hp
        self.weapon_equipment = None
        self.armor_equipment = None

    @property
    def equipped(self) -> bool:
        return self.armor_equipment != None

    @property
    def armed(self) -> bool:
        return self.weapon_equipment != None

    def equip(self, equipment: Equipment) -> Equipment|None:
        if isinstance(equipment, Weapon):
            prev = self.weapon_equipment
            self.weapon_equipment=equipment
            return prev
        if isinstance(equipment, Wearable):
            prev = self.armor_equipment
            self.armor_equipment=equipment
            return prev

    def unequip_weapon(self) -> Equipment|None:
        prev = copy.deepcopy(self.weapon_equipment)
        if self.weapon_equipment == self.armor_equipment:
            self.armor_equipment = None
        self.weapon_equipment = None
        return prev

    def unequip_armor(self) -> Equipment|None:
        prev = copy.deepcopy(self.armor_equipment)
        if self.armor_equipment == self.weapon_equipment:
            self.weapon_equipment = None
        self.armor_equipment = None
        return prev

    def __repr__(self) -> str:
        return f"{self.name.title()}-{self.hp} hp-{'equipped' if self.equipped else 'unequipped'} {'and armed' if self.armed else 'but unarmed'}"


class BodyParts:
    _parts: list[BodyPart]

    def __init__(self, *parts) -> None:
        self._parts = list(parts)

    def equip(self, equipment: Equipment) -> None:
        for part in self._parts:
            part.equip(equipment)

    def unequip(self) -> Equipment|None:
        for part in self._parts:
            part.unequip_weapon() #TODO: handle this return
            part.unequip_armor() #TODO: handle this return

    def __iter__(self):
        return iter(self._parts)

    def __sizeof__(self) -> int:
        return self._parts.__sizeof__()

    def __len__(self) -> int:
        return self._parts.__len__()


class Body:
    _hp: int
    alive: bool

    head: BodyPart
    torso: BodyPart
    left_arm: BodyPart
    left_hand: BodyPart
    right_arm: BodyPart
    right_hand: BodyPart
    left_leg: BodyPart
    left_foot: BodyPart
    right_leg: BodyPart
    right_foot: BodyPart

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value) -> None:
        if value < 0:
            self._hp = 0
        else:
            self._hp = value

    @property
    def parts(self) -> BodyParts:
        return BodyParts(self.head, self.torso, self.left_arm, self.left_hand,
                         self.right_arm, self.right_hand, self.left_leg,
                         self.left_foot, self.right_leg, self.right_foot)

    def parts_not_destroyed(self) -> BodyParts:
        return BodyParts(*[part for part in self.parts if part.hp > 0])

    @property
    def hands(self) -> BodyParts:
        return BodyParts(self.right_hand, self.left_hand)

    @property
    def arms(self) -> BodyParts:
        return BodyParts(self.right_arm, self.left_arm)

    @property
    def feet(self) -> BodyParts:
        return BodyParts(self.right_foot, self.left_foot)

    @property
    def legs(self) -> BodyParts:
        return BodyParts(self.right_leg, self.left_leg)

    def __init__(self, hp) -> None:
        self.hp = hp
        self.head = BodyPart("head")
        self.torso = BodyPart("torso")
        self.left_arm = BodyPart("left arm")
        self.left_hand = BodyPart("left hand")
        self.right_arm = BodyPart("right arm")
        self.right_hand = BodyPart("right_hand")
        self.left_leg = BodyPart("left leg")
        self.left_foot = BodyPart("left foot")
        self.right_leg = BodyPart("right leg")
        self.right_foot = BodyPart("right foot")

        for part in self.parts:
            part.hp = (self.hp // len(self.parts)) or 1


    def equip(self, *equipment:Equipment) -> None:
        for piece in equipment:
            if isinstance(piece, Weapon):
                self.hands.equip(piece)
            elif isinstance(piece, Wearable):
                if 'hand' in piece.wear_location:
                    self.hands.equip(piece)
                elif 'foot' in piece.wear_location:
                    self.feet.equip(piece)
                elif any(x in piece.wear_location for x in ('chest','torso')):
                    self.torso.equip(piece)
                elif 'leg' in piece.wear_location:
                    self.legs.equip(piece)
                elif 'arm' in piece.wear_location:
                    self.arms.equip(piece)

    def __repr__(self):
        return "\n".join(str(part) for part in self.parts)