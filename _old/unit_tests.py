import unittest
import copy

from dynamic.character import Character
from dynamic.stats import Stat
from dynamic.weapons import Sword


class CharacterTests(unittest.TestCase):

    def setUp(self) -> None:
        self.character = Character("TestCharacter")

    def test_sheet(self):
        self.assertTrue(isinstance(self.character.character_sheet, str),
                        "Character.character_sheet is not returning a string")

    def test_stats(self):
        self.assertTrue(
            all(name in list(map(lambda s: s.name, self.character.stats))
                for name in [
                    'strength', 'dexterity', 'constitution', 'wisdom',
                    'intelligence', 'charisma'
                ]), "missing some stat(s) from character.stats")

    def test_stat_values(self):
        self.assertTrue(
            all(3 <= stat.value <= 18 for stat in self.character.stats))

    def test_stat_comparisons(self):
        stat = Stat("Chonkiness", 20)
        stat2 = Stat("Chonkiness", 5)
        self.assertEqual(stat, 20)
        self.assertNotEqual(stat, stat2)
        self.assertGreater(stat, stat2)
        self.assertLess(stat2, stat)

    def test_stats_reroll(self):
        stats = copy.deepcopy(self.character.stats)
        self.character.stats.reroll_all()
        self.assertNotEqual(stats, self.character.stats)
        self.assertRaises(TypeError, lambda _: self.character.stats == 3)

    def test_equip_weapon(self):
        sword = Sword()
        self.character.equip(sword)

if __name__ == "__main__":
    unittest.main()