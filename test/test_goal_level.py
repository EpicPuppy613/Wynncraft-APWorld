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
            for location in self.multiworld.get_locations():
                with self.subTest("Location should be reached", location=location.name):
                    reachable = location.can_reach(state)
                    self.assertTrue(reachable, f"{location.name} unreachable")
            with self.subTest("Beatable"):
                self.multiworld.state = state
                self.assertBeatable(True)