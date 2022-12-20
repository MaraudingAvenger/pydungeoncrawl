from equipment import Gear, GearSet

class ClothArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Cloth Armor",
            description="A simple set of cloth armor.",
        )
        self.gear = [
            Gear(category="head", name="Cloth Hood", bonus_damage_received_percent=-0.01),
            Gear(category="chest", name="Cloth Robe", bonus_damage_received_percent=-0.01),
            Gear(category="legs", name="Cloth Pants", bonus_damage_received_percent=-0.01),
            Gear(category="feet", name="Cloth Shoes", bonus_damage_received_percent=-0.01),
            Gear(category="hands", name="Cloth Gloves", bonus_damage_received_percent=-0.01),
        ]


class LeatherArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Leather Armor",
            description="A creaky set of leather armor.",
        )
        self.gear = [
            Gear(category="head", name="Leather Hood", bonus_damage_received_percent=-0.02),
            Gear(category="chest", name="Leather Robe", bonus_damage_received_percent=-0.02),
            Gear(category="legs", name="Leather Pants", bonus_damage_received_percent=-0.02),
            Gear(category="feet", name="Leather Shoes", bonus_damage_received_percent=-0.02),
            Gear(category="hands", name="Leather Gloves", bonus_damage_received_percent=-0.02),
        ]

class ChainmailArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Chainmail Armor",
            description="A jingly set of chainmail armor.",
        )
        self.gear = [
            Gear(category="head", name="Chainmail Hood", bonus_damage_received_percent=-0.03),
            Gear(category="chest", name="Chainmail Robe", bonus_damage_received_percent=-0.03),
            Gear(category="legs", name="Chainmail Pants", bonus_damage_received_percent=-0.03),
            Gear(category="feet", name="Chainmail Shoes", bonus_damage_received_percent=-0.03),
            Gear(category="hands", name="Chainmail Gloves", bonus_damage_received_percent=-0.03),
        ]

class PlateArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Plate Armor",
            description="A shiny set of plate armor.",
        )
        self.gear = [
            Gear(category="head", name="Plate Hood", bonus_damage_received_percent=-0.04),
            Gear(category="chest", name="Plate Robe", bonus_damage_received_percent=-0.04),
            Gear(category="legs", name="Plate Pants", bonus_damage_received_percent=-0.04),
            Gear(category="feet", name="Plate Shoes", bonus_damage_received_percent=-0.04),
            Gear(category="hands", name="Plate Gloves", bonus_damage_received_percent=-0.04),
        ]

class MithrilArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Mithril Armor",
            description="A beautiful set of mithril armor.",
        )
        self.gear = [
            Gear(category="head", name="Mithril Hood", bonus_damage_received_percent=-0.05),
            Gear(category="chest", name="Mithril Robe", bonus_damage_received_percent=-0.05),
            Gear(category="legs", name="Mithril Pants", bonus_damage_received_percent=-0.05),
            Gear(category="feet", name="Mithril Shoes", bonus_damage_received_percent=-0.05),
            Gear(category="hands", name="Mithril Gloves", bonus_damage_received_percent=-0.05),
        ]

class AdamantiteArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Adamantite Armor",
            description="A set of hardened adamantite armor.",
        )
        self.gear = [
            Gear(category="head", name="Adamantite Hood", bonus_damage_received_percent=-0.06),
            Gear(category="chest", name="Adamantite Robe", bonus_damage_received_percent=-0.06),
            Gear(category="legs", name="Adamantite Pants", bonus_damage_received_percent=-0.06),
            Gear(category="feet", name="Adamantite Shoes", bonus_damage_received_percent=-0.06),
            Gear(category="hands", name="Adamantite Gloves", bonus_damage_received_percent=-0.06),
        ]

class RuniteArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Runite Armor",
            description="A resplendent set of runite armor.",
        )
        self.gear = [
            Gear(category="head", name="Runite Hood", bonus_damage_received_percent=-0.07),
            Gear(category="chest", name="Runite Robe", bonus_damage_received_percent=-0.07),
            Gear(category="legs", name="Runite Pants", bonus_damage_received_percent=-0.07),
            Gear(category="feet", name="Runite Shoes", bonus_damage_received_percent=-0.07),
            Gear(category="hands", name="Runite Gloves", bonus_damage_received_percent=-0.07),
        ]

class DragonArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Dragon Armor",
            description="A master-crafted set of dragon armor.",
        )
        self.gear = [
            Gear(category="head", name="Dragon Hood", bonus_damage_received_percent=-0.08),
            Gear(category="chest", name="Dragon Robe", bonus_damage_received_percent=-0.08),
            Gear(category="legs", name="Dragon Pants", bonus_damage_received_percent=-0.08),
            Gear(category="feet", name="Dragon Shoes", bonus_damage_received_percent=-0.08),
            Gear(category="hands", name="Dragon Gloves", bonus_damage_received_percent=-0.08),
        ]

class DemonArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Demon Armor",
            description="A set of armor forged from the bones of demons.",
        )
        self.gear = [
            Gear(category="head", name="Demon Hood", bonus_damage_received_percent=-0.09),
            Gear(category="chest", name="Demon Robe", bonus_damage_received_percent=-0.09),
            Gear(category="legs", name="Demon Pants", bonus_damage_received_percent=-0.09),
            Gear(category="feet", name="Demon Shoes", bonus_damage_received_percent=-0.09),
            Gear(category="hands", name="Demon Gloves", bonus_damage_received_percent=-0.09),
        ]

class GodArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="God Armor",
            description="A set of armor given to mortals by the gods.",
        )
        self.gear = [
            Gear(category="head", name="God Hood", bonus_damage_received_percent=-0.10),
            Gear(category="chest", name="God Robe", bonus_damage_received_percent=-0.10),
            Gear(category="legs", name="God Pants", bonus_damage_received_percent=-0.10),
            Gear(category="feet", name="God Shoes", bonus_damage_received_percent=-0.10),
            Gear(category="hands", name="God Gloves", bonus_damage_received_percent=-0.10),
        ]