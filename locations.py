from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items
from .data import loader

if TYPE_CHECKING:
    from .world import WynncraftWorld

location_name_to_id = {}
location_name_to_classification = {}

for _row in loader.rows:
    if _row[loader.AP] != "Location" or _row[loader.ID] == "":
        continue
    location_id = int(_row[loader.ID].replace(" ", ""), 16)
    name = _row[loader.NAME]
    location_name_to_id[name] = location_id

class WynncraftLocation(Location):
    game = "Wynncraft"


def create_all_locations(world: WynncraftWorld) -> None:
    for row in loader.rows:
        if row[loader.AP] != "Location" or row[loader.ID] == "" or row[loader.LEVEL] == "" or int(row[loader.LEVEL]) >= world.options.goal_level:
            continue

        if not world.location_enabled(row[loader.TYPE]) and row[loader.IS_PREREQ] == "FALSE":
            continue

        if row[loader.REGION] != "" and row[loader.TYPE] != "Level":
            region = world.get_region(row[loader.REGION].split(", ")[0])
        elif row[loader.TYPE] == "Level":
            region = world.get_region("Level " + row[loader.LEVEL])
        else:
            region = world.get_region("Menu")

        if not world.location_enabled(row[loader.TYPE]) and row[loader.IS_PREREQ] == "TRUE":
            region.add_event(row[loader.NAME], "-", location_type=WynncraftLocation, item_type=items.WynncraftItem, show_in_spoiler=False)
        else:
            location = WynncraftLocation(world.player, row[loader.NAME], world.location_name_to_id[row[loader.NAME]], region)
            region.locations.append(location)

    world.get_region("Level " + str(world.options.goal_level)).add_event(
        "Level Up: " + str(world.options.goal_level), "Victory", location_type=WynncraftLocation, item_type=items.WynncraftItem
    )