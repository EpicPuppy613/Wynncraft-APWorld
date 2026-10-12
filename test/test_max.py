from worlds.wynncraft.test.bases import WynncraftTestBase


class TestMaxSettings(WynncraftTestBase):
    options = {
        "goal_level": "121",
        "region_lock_mode": "full",
        "gear_lock_mode": "full",
        "corrupted_dungeon_checks": "true",
        "raid_checks": "true"
    }