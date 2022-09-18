from dungeoncrawl.factories.names import NameFactory

# TODO: I want this to be able to take a list of different
# types of loot to be able to generate from a specific source.
# I also want this to come preloaded with a set of "default"
# loot so it doesn't have to be loaded if the DM doesn't want to.


class LootFactory:
    def __init__(self) -> None:
        self.name_factory = NameFactory()
        
        