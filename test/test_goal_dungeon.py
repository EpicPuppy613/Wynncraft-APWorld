from worlds.wynncraft.test.bases import WynncraftTestBase


class TestGoalDungeonChoice(WynncraftTestBase):
    options = {
        "goal_type": "dungeon",
        "goal_dungeon": "tomb"
    }

    def test_goal_dungeon_choice_matches(self):
        self.assertEqual(self.world.goal_dungeon, "Complete: Sand-Swept Tomb", "Goal quest must be 'Complete: Sand-Swept Tomb'")

    def test_goal_dungeon_choice_level(self):
        self.assertEqual(self.world.max_level, 36, "Goal level must be 36")


class TestGoalDungeonName(WynncraftTestBase):
    options = {
        "goal_type": "dungeon",
        "goal_dungeon": "Corrupted Decrepit Sewers"
    }

    def test_goal_dungeon_name_matches(self):
        self.assertEqual(self.world.goal_dungeon, "Complete: Corrupted Decrepit Sewers", "Goal quest must be 'Complete: Corrupted Decrepit Sewers'")

    def test_goal_dungeon_name_level(self):
        self.assertEqual(self.world.max_level, 70, "Goal level must be 70")