from test.bases import WorldTestBase

class WynncraftTestBase(WorldTestBase):
    game = "Wynncraft"

class WynncraftTestNoDefaultBase(WorldTestBase):
    game = "Wynncraft"

    @property
    def run_default_tests(self) -> bool:
        return False

class WynncraftAccessibilityBase(WynncraftTestNoDefaultBase):
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