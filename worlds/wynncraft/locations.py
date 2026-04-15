from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items
from .data import loader

if TYPE_CHECKING:
    from .world import WynncraftWorld

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
location_name_to_id = {}
location_name_to_classification = {}

for row in loader.rows:
    if row[loader.AP] != 'Location' or row[loader.ID] == '':
        continue
    location_id = int(row[loader.ID].replace(" ", ""), 16)
    name = row[loader.NAME]
    location_name_to_id[name] = location_id

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class WynncraftLocation(Location):
    game = "Wynncraft"


def create_all_locations(world: WynncraftWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: WynncraftWorld) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    for row in loader.rows:
        if row[loader.AP] != 'Location' or row[loader.ID] == '':
            continue

        if row[loader.REGION] != '':
            region = world.get_region(row[loader.REGION])
        else:
            region = world.get_region("Menu")

        location = WynncraftLocation(world.player, row[loader.NAME], world.location_name_to_id[row[loader.NAME]], region)
        region.locations.append(location)


def create_events(world: WynncraftWorld) -> None:
    # Sometimes, the player may perform in-game actions that allow them to progress which are not related to Items.
    # In our case, the player must press a button in the top left room to open the final boss door.
    # AP has something for this purpose: "Event locations" and "Event items".
    # An event location is no different than a regular location, except it has the address "None".
    # It is treated during generation like any other location, but then it is discarded.
    # This location cannot be "sent" and its item cannot be "received", but the item can be used in logic rules.
    # Since we are creating more locations and adding them to regions, we need to grab those regions again first.


    # If you create all your regions and locations line-by-line like this,
    # the length of your create_regions might get out of hand.
    # Many worlds use more data-driven approaches using dataclasses or NamedTuples.
    # However, it is worth understanding how the actual creation of regions and locations works,
    # That way, we're not just mindlessly copy-pasting! :)

    world.get_region("Menu").add_event(
        "Level Up: 20", "Victory", location_type=WynncraftLocation, item_type=items.WynncraftItem
    )

    pass
