from Options import OptionError
from worlds.wynncraft.test.bases import WynncraftTestBase, WynncraftTestNoDefaultBase


class TestGoalQuestChoice(WynncraftTestBase):
    options = {
        "goal_type": "quest",
        "goal_quest": "llevigar"
    }

    def test_goal_quest_choice_matches(self):
        self.assertEqual(self.world.goal_quest, "Complete: Heart of Llevigar", "Goal quest must be 'Complete: Heart of Llevigar'")

    def test_goal_quest_choice_level(self):
        self.assertEqual(self.world.max_level, 41, "Goal level must be 41")


class TestGoalQuestName(WynncraftTestBase):
    options = {
        "goal_type": "quest",
        "goal_quest": "An Iron Heart Part I"
    }

    def test_goal_quest_name_matches(self):
        self.assertEqual(self.world.goal_quest, "Complete: An Iron Heart Part I", "Goal quest must be 'Complete: An Iron Heart Part I'")

    def test_goal_quest_name_level(self):
        self.assertEqual(self.world.max_level, 49, "Goal level must be 49")


class TestGoalQuestInvalid(WynncraftTestNoDefaultBase):
    options = {
        "goal_type": "quest",
        "goal_quest": "some quest that i made up idk"
    }

    auto_construct = False

    def test_invalid_quest_raises_error(self):
        self.assertRaises(OptionError, self.world_setup)