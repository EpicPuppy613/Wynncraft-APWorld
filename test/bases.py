from test.bases import WorldTestBase

class WynncraftTestBase(WorldTestBase):
    game = "Wynncraft"

class WynncraftTestNoDefaultBase(WorldTestBase):
    game = "Wynncraft"

    @property
    def run_default_tests(self) -> bool:
        return False