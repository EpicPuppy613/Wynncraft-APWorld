from __future__ import annotations

from typing import TYPE_CHECKING

from math import ceil

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from . import WynncraftWorld

from .data import loader

if TYPE_CHECKING:
    from .world import WynncraftWorld


def set_all_rules(world: WynncraftWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: WynncraftWorld) -> None:
    for row in loader.rows:
        if row[loader.TYPE] != "Territory" or row[loader.CONNECTIONS] == "":
            continue
        for connection in row[loader.CONNECTIONS].split(", "):
            entrance = world.get_entrance(f"{row[loader.NAME]} to {connection}")
            if connection in loader.unlockable_regions:
                set_rule(entrance, lambda state: state.has(f"Region: {connection}", world.player))


def set_all_location_rules(world: WynncraftWorld) -> None:
    for row in loader.rows:
        if row[loader.AP] != "Location":
            continue

        regions = row[loader.REGION].split(", ")
        location = world.get_location(row[loader.NAME])
        if len(regions) > 1:
            del regions[0]
            for region in regions:
                add_rule(location, lambda state: state.can_reach_region(region, world.player))


        levels_needed = ceil(int(row[loader.LEVEL]) / 5) - 1
        if levels_needed > 0:
            add_rule(world.get_location(row[loader.NAME]), lambda state: state.has("Progressive Max Level", world.player, levels_needed))


def set_completion_condition(world: WynncraftWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
