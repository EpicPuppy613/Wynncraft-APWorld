from collections.abc import Mapping
from typing import Any

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
        return {}
        # return self.options.as_dict(
        #     "hard_mode", "hammer", "extra_starting_chest", "confetti_explosiveness", "player_sprite"
        # )
