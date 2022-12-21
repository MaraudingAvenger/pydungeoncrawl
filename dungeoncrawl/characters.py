
from dungeoncrawl.entities.pawn import Pawn
from dungeoncrawl.entities.effects import Effect
from dungeoncrawl.utilities.location import Point
from dungeoncrawl.armor import ClothArmor


class Character(Pawn):
    def __init__(self, name: str, symbol: str, role: str, position: Point | tuple[int, int] = Point(0,0), health_max: int = 100) -> None:
        super().__init__(name, position, health_max, symbol)
        self.name = name
        self.role = role
   
    def __repr__(self):
        return f"Character({self.name}, {self.position}, {self.health_max}, {self._symbol})"

    def __str__(self):
        return f"Character({self.name}, {self.position}, {self.health_max}, {self._symbol})"


#TODO change the name of this excellent function
def _WITNESS_MEEEEE(func):
    def wrapper(self, *args, **kwargs):
        self.action = True
        print(f"{self.__class__.__name__}.{func.__name__}({args}, {kwargs}) has been witnessed")
        self.action_history.append(f"{self.__class__.__name__} used {func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper

class DummyHero(Character):
    def __init__(self, name: str) -> None:
        super().__init__(name, '🚶', 'tank', (0,0), 100)
        self.equip(ClothArmor())
        self.turn = None
        self.action = False

    @_WITNESS_MEEEEE
    def ball_punch(self, target: Character) -> None:
        target._take_damage(20)
        target.effects.add(Effect(name="Dummy Hero Ball Punch", duration=5, heal_over_time=2))

    def __repr__(self):
        return f"DummyHero({self.name}, {self.position}, {self.health}/{self.health_max}, {self._symbol})"

    def __str__(self):
        return f"DummyHero({self.name}, {self.position}, {self.health}/{self.health_max}, {self._symbol})"


class Party:
    def __init__(self, members: tuple[Character,...]|list[Character]) -> None:
        self.members = members
        
        if len((twalrus := list(filter(lambda x: x.role.lower() == 'tank', members)))) != 1:
            raise ValueError("Party must have exactly one tank")
        self._tank = twalrus[0]
        

        
        # if len((twalrus := list(filter(lambda x: x.role.lower() == 'healer', members)))) != 1:
        #     raise ValueError("Party must have exactly one healer")
        # self._healer = twalrus[0]
        
        # if len((twalrus := list(filter(lambda x: x.role.lower() == 'dps', members)))) != 2:
        #     raise ValueError("Party must have at least two dps")
        # self._dps = tuple(twalrus)
        
    def tick(self):
        #TODO: add logic for party-wide effects
        for member in self.members:
            member.tick()
    
    @property
    def tank(self) -> Pawn:
        return self._tank

    # @property
    # def healer(self) -> Pawn:
    #     return self._healer

    # @property
    # def dps(self) -> tuple[Pawn, ...]:
    #     return self._dps

    def is_alive(self) -> bool:
        return all(member._is_dead for member in self.members)

    def __repr__(self):
        return f"Party({self.members})"

    def __str__(self):
        return f"Party({self.members})"

    def __iter__(self):
        return iter(self.members)


