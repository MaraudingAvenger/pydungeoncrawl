from dungeoncrawl.entities.equipment import Gear

class Mace(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Mace",
            description="A heavy mace.",
            damage=5,
            damage_type="physical",
        )

class Sword(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Sword",
            description="A sharp sword.",
            damage=6,
            damage_type="physical",
        )

class Axe(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Axe",
            description="A sharp axe.",
            damage=7,
            damage_type="physical",
        )

class SideKnife(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="offhand",
            name="Side Knife",
            description="A small knife.",
            damage=2,
            damage_type="physical",
        )

class Dagger(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Dagger",
            description="A sharp dagger.",
            damage=4,
            damage_type="physical",
        )

class Staff(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Staff",
            description="A wooden staff.",
            damage=3,
            damage_type="physical",
        )

class ShortBow(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Short Bow",
            description="A short bow.",
            damage=5,
            damage_type="physical",
        )

class Claymore(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Claymore",
            description="A large, two-handed sword.",
            damage=8,
            damage_type="physical",
        )

class Lute(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Lute",
            description = "A guitar-like musical instrument.",
            damage = 2,
            damage_type = "physical"
        )