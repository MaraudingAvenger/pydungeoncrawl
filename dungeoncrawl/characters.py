from dungeoncrawl.entities.pawn import Pawn, Action, _action_decorator
from dungeoncrawl.entities.effects import Effect
from dungeoncrawl.utilities.location import Point
from dungeoncrawl.armor import ClothArmor


class Character(Pawn):
    def __init__(self, name: str, symbol: str, role: str, position: Point | tuple[int, int] = Point(0, 0), health_max: int = 100) -> None:
        super().__init__(name, position, health_max, symbol)
        self.name = name
        self.role = role
        self.ability_cooldowns: dict[str, int] = {}

    @property
    def last_action(self) -> Action | None:
        if self.action_history:
            return self.action_history[-1]

    @property
    def last_successful_action(self) -> Action | None:
        for action in reversed(self.action_history):
            if not action.failed:
                return action

    def __repr__(self):
        return f"Character({self.name}, {self.position}, {self.health_max}, {self._symbol})"

    def __str__(self):
        return f"Character({self.name}, {self.position}, {self.health_max}, {self._symbol})"


class DummyHero(Character):
    def __init__(self, name: str, position: Point | tuple[int, int], role, symbol:str='🍄') -> None:
        super().__init__(name, symbol, role, position, 100)
        self.equip(ClothArmor())
        self.turn = None

    @_action_decorator(cooldown=2, melee=True)
    def ball_punch(self, target: Pawn) -> None:
        target._take_damage(100)
        target.effects.add(Effect(name="Dummy Hero Ball Punch", duration=5))


class Party:
    def __init__(self, *members: Character) -> None:
        self.members = members

        # check that they don't have more than one of one type of class
        # for member in members:
        #     for other in members:
        #         if (member is not other and
        #         member.__class__.__name__ == other.__class__.__name__):
        #             raise ValueError("Party must be made up of unique classes")

        if len((walrus := list(filter(lambda x: x.role.lower() == 'tank', members)))) != 1:
            raise ValueError("Party must have exactly one tank")
        self._tank = walrus[0]

        if len((walrus := list(filter(lambda x: x.role.lower() == 'healer', members)))) != 1:
            raise ValueError("Party must have exactly one healer")
        self._healer = walrus[0]

        if len((walrus := list(filter(lambda x: x.role.lower() == 'dps', members)))) != 2:
            raise ValueError("Party must have at least two dps")
        self._dps = tuple(walrus)

    def _tick(self):
        for member in self.members:
            member._tick()

    def _add_effect(self, effect: Effect):
        for member in self.members:
            member.effects.add(effect)

    @property
    def tank(self) -> Pawn:
        return self._tank

    @property
    def healer(self) -> Pawn:
        return self._healer

    @property
    def dps(self) -> tuple[Pawn, ...]:
        return self._dps

    @property
    def is_alive(self) -> bool:
        return any(member.is_alive for member in self.members)

    @property
    def is_dead(self) -> bool:
        return not self.is_alive

    def __repr__(self):
        return f"Party({self.members})"

    def __str__(self):
        return f"Party({self.members})"

    def __iter__(self):
        return iter(self.members)

    def __getitem__(self, key):
        return [member
                for member in self.members
                if member.name.lower() == key.lower()
                or key.lower() in member.__class__.__name__.lower()][0]
