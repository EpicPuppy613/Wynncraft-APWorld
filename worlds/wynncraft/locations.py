from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items
from .data import loader

if TYPE_CHECKING:
    from .world import WynncraftWorld

location_name_to_id = {}
location_name_to_classification = {}

for row in loader.rows:
    if row[loader.AP] != 'Location' or row[loader.ID] == '':
        continue
    location_id = int(row[loader.ID].replace(" ", ""), 16)
    name = row[loader.NAME]
    location_name_to_id[name] = location_id

class WynncraftLocation(Location):
    game = "Wynncraft"


def create_all_locations(world: WynncraftWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: WynncraftWorld) -> None:
    for row in loader.rows:
        if row[loader.AP] != 'Location' or row[loader.ID] == '':
            continue

        if row[loader.REGION] != '':
            region = world.get_region(row[loader.REGION].split(", ")[0])
        else:
            region = world.get_region("Menu")

        location = WynncraftLocation(world.player, row[loader.NAME], world.location_name_to_id[row[loader.NAME]], region)
        region.locations.append(location)


def create_events(world: WynncraftWorld) -> None:
    world.get_region("Menu").add_event(
        "Level Up: 20", "Victory", location_type=WynncraftLocation, item_type=items.WynncraftItem
    )
