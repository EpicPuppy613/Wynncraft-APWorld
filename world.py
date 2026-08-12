from collections.abc import Mapping
from typing import Any

from BaseClasses import MultiWorld
from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world
from . import options as wynncraft_options  # rename due to a name conflict with World.options


class WynncraftWorld(World):
    """
    Wynncraft is a Minecraft MMORPG with completely custom abilities and combat.
    """

    game = "Wynncraft"

    web = web_world.WynncraftWebWorld()

    options_dataclass = wynncraft_options.WynncraftOptions
    options: wynncraft_options.WynncraftOptions

    location_name_to_id = locations.location_name_to_id
    item_name_to_id = items.item_name_to_id

    origin_region_name = "Menu"

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.all_regions = []
        self.unlockable_regions = []

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.WynncraftItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "goal_level", "level_increment", "trap_duration",
            "gear_lock_mode", "single_gear_rarity", "gear_level_increment",
            "locked_region_enforcement", "locked_region_countdown"
        )

    def location_enabled(self, type):
        if type == "Quest" and not self.options.quest_checks:
            return False

        if type == "Mini-Quest" and not self.options.mini_quest_checks:
            return False

        if type == "Dungeon" and not self.options.dungeon_checks:
            return False

        if type == "Cave" and not self.options.cave_checks:
            return False

        if type == "Level" and not self.options.level_checks:
            return False

        if type == "Territory" and not self.options.territory_checks:
            return False

        return True