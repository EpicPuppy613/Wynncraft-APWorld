import typing

from test.param import classvar_matrix
from worlds.wynncraft.options import GoalLevel
from worlds.wynncraft.test.bases import WynncraftTestNoDefaultBase

@classvar_matrix(level = range(GoalLevel.range_start, GoalLevel.range_end + 1))
class TestGoalLevel(WynncraftTestNoDefaultBase):
    level: typing.ClassVar[int]
    
    def setUp(self) -> None:
        self.options["goal_level"] = self.level
        super().setUp()

    def test_goal_level_matches_max_level(self):
        self.assertEqual(self.world.max_level, self.level - 1, "Max level must be " + str(self.level - 1))
        
    def test_level_all_state_can_reach_everything(self):
        with self.subTest("Game", game=self.game, seed=self.multiworld.seed):
            state = self.multiworld.get_all_state()
            with self.subTest("Reaches all locations"):
                failures = []
                for location in self.multiworld.get_locations():
                    reachable = location.can_reach(state)
                    if not reachable:
                        failures.append(location.name)
                self.assertTrue(len(failures) == 0, f"{failures} unreachable")
            with self.subTest("Reaches all regions"):
                failures = []
                for region in self.multiworld.get_regions():
                    reachable = region.can_reach(state)
                    if not reachable:
                        failures.append(region.name)
                self.assertTrue(len(failures) == 0, f"{failures} unreachable")
            with self.subTest("Beatable"):
                self.multiworld.state = state
                self.assertBeatable(True)