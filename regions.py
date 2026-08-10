from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

from .data import loader

if TYPE_CHECKING:
    from .world import WynncraftWorld

def create_and_connect_regions(world: WynncraftWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: WynncraftWorld) -> None:
    regions = [Region("Menu", world.player, world.multiworld)]

    for row in loader.rows:
        if row[loader.TYPE] != "Region" or row[loader.NAME].startswith("*"):
            continue

        if int(row[loader.LEVEL]) >= world.options.goal_level:
            continue

        regions.append(Region(row[loader.NAME], world.player, world.multiworld))
        world.all_regions.append(row[loader.NAME])

        if row[loader.AP] == "Item":
            world.unlockable_regions.append(row[loader.NAME])

    world.multiworld.regions += regions


def connect_regions(world: WynncraftWorld) -> None:
    for row in loader.rows:
        if row[loader.TYPE] != "Region" or row[loader.NAME].startswith("*"):
            continue
        if int(row[loader.LEVEL]) >= world.options.goal_level:
            continue
        if row[loader.CONNECTIONS] == "":
            continue

        region = world.get_region(row[loader.NAME])
        for connection in row[loader.CONNECTIONS].split(", "):
            if connection in world.all_regions:
                region.connect(world.get_region(connection), f"{row[loader.NAME]} to {connection}")

    # Connection from default region to starting region in game (Ragni)
    world.get_region("Menu").connect(world.get_region("Ragni"), "Menu to Ragni")
