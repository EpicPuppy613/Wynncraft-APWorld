from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

from .data import loader

if TYPE_CHECKING:
    from .world import WynncraftWorld

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: WynncraftWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: WynncraftWorld) -> None:
    regions = [Region("Menu", world.player, world.multiworld)]

    for row in loader.rows:
        if row[loader.TYPE] != "Territory":
            continue
        regions.append(Region(row[loader.NAME], world.player, world.multiworld))

    world.multiworld.regions += regions


def connect_regions(world: WynncraftWorld) -> None:
    for row in loader.rows:
        if row[loader.TYPE] != "Territory" or row[loader.CONNECTIONS] == "":
            continue
        region = world.get_region(row[loader.NAME])
        for connection in row[loader.CONNECTIONS].split(", "):
            region.connect(world.get_region(connection), f"{row[loader.NAME]} to {connection}")

    # Connection from default region to starting region in game (Ragni)
    world.get_region("Menu").connect(world.get_region("Ragni"), "Menu to Ragni")
