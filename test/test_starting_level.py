import typing

from test.param import classvar_matrix
from worlds.wynncraft.options import StartingMaxLevel
from worlds.wynncraft.test.bases import WynncraftAccessibilityBase

@classvar_matrix(level = range(StartingMaxLevel.range_start, StartingMaxLevel.range_end + 1))
class TestStartingLevel(WynncraftAccessibilityBase):
    level: typing.ClassVar[int]
    options = {
        "goal_level": 121,
        "extra_max_levels": 0
    }

    def setUp(self) -> None:
        self.options["starting_max_level"] = self.level
        super().setUp()

    def test_correct_number_of_level_items(self):
        self.assertEqual(self.multiworld.get_all_state().count("Progressive Max Level", self.world.player), 121 - self.level)
