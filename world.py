from collections.abc import Mapping
from typing import Any

from Options import OptionError
from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world
from . import options as wynncraft_options  # rename due to a name conflict with World.options
from .data.loader import all_dungeons, all_quests
from .options import default_dungeon_map, default_quest_map


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

    all_regions: list[str]
    unlockable_regions: list[str]
    max_level: int
    goal_dungeon: str
    goal_quest: str

    is_level_goal: bool
    is_dungeon_goal: bool
    is_quest_goal: bool

    def generate_early(self) -> None:
        self.all_regions = []
        self.unlockable_regions = []

        if self.options.goal_type == self.options.goal_type.option_level:
            self.max_level = self.options.goal_level - 1

        elif self.options.goal_type == self.options.goal_type.option_dungeon:
            if isinstance(self.options.goal_dungeon.value, int):
                if not int(self.options.goal_dungeon) in default_dungeon_map:
                    raise OptionError("Invalid dungeon choice")
                dungeon = default_dungeon_map[int(self.options.goal_dungeon)]

            else:
                if not str(self.options.goal_dungeon.value) in all_dungeons:
                    raise OptionError("Could not find dungeon: " + str(self.options.goal_dungeon.value))
                dungeon = str(self.options.goal_dungeon.value)

            self.goal_dungeon = "Complete: " + dungeon
            self.max_level = all_dungeons[dungeon]

        elif self.options.goal_type == self.options.goal_type.option_quest:
            if isinstance(self.options.goal_quest.value, int):
                if not int(self.options.goal_quest) in default_quest_map:
                    raise OptionError("Invalid quest choice")
                quest = default_quest_map[int(self.options.goal_quest)]

            else:
                if not str(self.options.goal_quest.value) in all_quests:
                    raise OptionError("Could not find quest: " + str(self.options.goal_quest.value))
                quest = str(self.options.goal_quest.value)

            self.goal_quest = "Complete: " + quest
            self.max_level = all_quests[quest]

        else:
            raise OptionError("Invalid objective")

        self.is_level_goal = self.options.goal_type == self.options.goal_type.option_level
        self.is_dungeon_goal = self.options.goal_type == self.options.goal_type.option_dungeon
        self.is_quest_goal = self.options.goal_type == self.options.goal_type.option_quest

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
        slot_data = self.options.as_dict(
            "goal_type",
            "goal_level",

            "locked_region_enforcement",
            "locked_region_countdown",

            "level_increment",
            "gear_lock_mode",
            "single_gear_rarity",
            "gear_level_increment",

            "quest_checks",
            "mini_quest_checks",
            "cave_checks",
            "dungeon_checks",
            "level_checks",
            "logical_levels",
            "territory_checks",
            "early_territory_levels",

            "trap_duration",

            "death_link"
        )

        if hasattr(self, "goal_dungeon"):
            slot_data["goal_dungeon"] = self.goal_dungeon
        else:
            slot_data["goal_dungeon"] = ""
        if hasattr(self, "goal_quest"):
            slot_data["goal_quest"] = self.goal_quest
        else:
            slot_data["goal_quest"] = ""

        slot_data["world_version"] = self.world_version.as_simple_string()

        return slot_data

    def location_enabled(self, loc_type):
        if loc_type == "Quest" and not self.options.quest_checks:
            return False

        if loc_type == "Mini-Quest" and not self.options.mini_quest_checks:
            return False

        if loc_type == "Dungeon" and not self.options.dungeon_checks:
            return False

        if loc_type == "Cave" and not self.options.cave_checks:
            return False

        if loc_type == "Level" and not self.options.level_checks:
            return False

        if loc_type == "Territory" and not self.options.territory_checks:
            return False

        return True