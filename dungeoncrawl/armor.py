from dungeoncrawl.entities.equipment import Gear, GearSet

class Shield(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="offhand",
            name="Shield",
            description="A sturdy shield.",
            damage_reduction_percent=0.05,
        )

class ClothArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Cloth Armor",
            description="A simple set of cloth armor.",
        )
        self.gear = [
            Gear(category="head", name="Cloth Hood", damage_reduction_percent=0.01),
            Gear(category="chest", name="Cloth Robe", damage_reduction_percent=0.01),
            Gear(category="legs", name="Cloth Pants", damage_reduction_percent=0.01),
            Gear(category="feet", name="Cloth Shoes", damage_reduction_percent=0.01),
            Gear(category="hands", name="Cloth Gloves", damage_reduction_percent=0.01),
        ]


class LeatherArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Leather Armor",
            description="A creaky set of leather armor.",
        )
        self.gear = [
            Gear(category="head", name="Leather Hood", damage_reduction_percent=0.02),
            Gear(category="chest", name="Leather Robe", damage_reduction_percent=0.02),
            Gear(category="legs", name="Leather Pants", damage_reduction_percent=0.02),
            Gear(category="feet", name="Leather Shoes", damage_reduction_percent=0.02),
            Gear(category="hands", name="Leather Gloves", damage_reduction_percent=0.02),
        ]

class ChainmailArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Chainmail Armor",
            description="A jingly set of chainmail armor.",
        )
        self.gear = [
            Gear(category="head", name="Chainmail Hood", damage_reduction_percent=0.03),
            Gear(category="chest", name="Chainmail Robe", damage_reduction_percent=0.03),
            Gear(category="legs", name="Chainmail Pants", damage_reduction_percent=0.03),
            Gear(category="feet", name="Chainmail Shoes", damage_reduction_percent=0.03),
            Gear(category="hands", name="Chainmail Gloves", damage_reduction_percent=0.03),
        ]

class PlateArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Plate Armor",
            description="A shiny set of plate armor.",
        )
        self.gear = [
            Gear(category="head", name="Plate Hood", damage_reduction_percent=0.04),
            Gear(category="chest", name="Plate Robe", damage_reduction_percent=0.04),
            Gear(category="legs", name="Plate Pants", damage_reduction_percent=0.04),
            Gear(category="feet", name="Plate Shoes", damage_reduction_percent=0.04),
            Gear(category="hands", name="Plate Gloves", damage_reduction_percent=0.04),
        ]

class MithrilArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Mithril Armor",
            description="A beautiful set of mithril armor.",
        )
        self.gear = [
            Gear(category="head", name="Mithril Hood", damage_reduction_percent=0.05),
            Gear(category="chest", name="Mithril Robe", damage_reduction_percent=0.05),
            Gear(category="legs", name="Mithril Pants", damage_reduction_percent=0.05),
            Gear(category="feet", name="Mithril Shoes", damage_reduction_percent=0.05),
            Gear(category="hands", name="Mithril Gloves", damage_reduction_percent=0.05),
        ]

class AdamantiteArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Adamantite Armor",
            description="A set of hardened adamantite armor.",
        )
        self.gear = [
            Gear(category="head", name="Adamantite Hood", damage_reduction_percent=0.06),
            Gear(category="chest", name="Adamantite Robe", damage_reduction_percent=0.06),
            Gear(category="legs", name="Adamantite Pants", damage_reduction_percent=0.06),
            Gear(category="feet", name="Adamantite Shoes", damage_reduction_percent=0.06),
            Gear(category="hands", name="Adamantite Gloves", damage_reduction_percent=0.06),
        ]

class RuniteArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Runite Armor",
            description="A resplendent set of runite armor.",
        )
        self.gear = [
            Gear(category="head", name="Runite Hood", damage_reduction_percent=0.07),
            Gear(category="chest", name="Runite Robe", damage_reduction_percent=0.07),
            Gear(category="legs", name="Runite Pants", damage_reduction_percent=0.07),
            Gear(category="feet", name="Runite Shoes", damage_reduction_percent=0.07),
            Gear(category="hands", name="Runite Gloves", damage_reduction_percent=0.07),
        ]

class DragonArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Dragon Armor",
            description="A master-crafted set of dragon armor.",
        )
        self.gear = [
            Gear(category="head", name="Dragon Hood", damage_reduction_percent=0.08),
            Gear(category="chest", name="Dragon Robe", damage_reduction_percent=0.08),
            Gear(category="legs", name="Dragon Pants", damage_reduction_percent=0.08),
            Gear(category="feet", name="Dragon Shoes", damage_reduction_percent=0.08),
            Gear(category="hands", name="Dragon Gloves", damage_reduction_percent=0.08),
        ]

class DemonArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="Demon Armor",
            description="A set of armor forged from the bones of demons.",
        )
        self.gear = [
            Gear(category="head", name="Demon Hood", damage_reduction_percent=0.09),
            Gear(category="chest", name="Demon Robe", damage_reduction_percent=0.09),
            Gear(category="legs", name="Demon Pants", damage_reduction_percent=0.09),
            Gear(category="feet", name="Demon Shoes", damage_reduction_percent=0.09),
            Gear(category="hands", name="Demon Gloves", damage_reduction_percent=0.09),
        ]

class GodArmor(GearSet):
    def __init__(self) -> None:
        super().__init__(
            name="God Armor",
            description="A set of armor given to mortals by the gods.",
        )
        self.gear = [
            Gear(category="head", name="God Hood", damage_reduction_percent=0.10),
            Gear(category="chest", name="God Robe", damage_reduction_percent=0.10),
            Gear(category="legs", name="God Pants", damage_reduction_percent=0.10),
            Gear(category="feet", name="God Shoes", damage_reduction_percent=0.10),
            Gear(category="hands", name="God Gloves", damage_reduction_percent=0.10),
        ]