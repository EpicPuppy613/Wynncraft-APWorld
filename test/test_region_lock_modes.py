from worlds.wynncraft.test.bases import WynncraftAccessibilityBase


class TestFullRegionLock(WynncraftAccessibilityBase):
    options = {
        "goal_level": 121,
        "region_lock_mode": "full"
    }

class TestZoneRegionLock(WynncraftAccessibilityBase):
    options = {
        "goal_level": 121,
        "region_lock_mode": "zones"
    }

class TestAreaRegionLock(WynncraftAccessibilityBase):
    options = {
        "goal_level": 121,
        "region_lock_mode": "areas"
    }

class TestNoRegionLock(WynncraftAccessibilityBase):
    options = {
        "goal_level": 121,
        "region_lock_mode": "off"
    }