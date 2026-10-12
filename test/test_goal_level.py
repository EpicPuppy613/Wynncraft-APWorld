import typing

from test.param import classvar_matrix
from worlds.wynncraft.options import GoalLevel
from worlds.wynncraft.test.bases import WynncraftAccessibilityBase


@classvar_matrix(level = range(GoalLevel.range_start, GoalLevel.range_end + 1))
class TestGoalLevel(WynncraftAccessibilityBase):
    level: typing.ClassVar[int]
    options = {
        "region_lock_mode": "full"
    }
    
    def setUp(self) -> None:
        self.options["goal_level"] = self.level
        super().setUp()

    def test_goal_level_matches_max_level(self):
        self.assertEqual(self.world.max_level, self.level - 1, "Max level must be " + str(self.level - 1))
