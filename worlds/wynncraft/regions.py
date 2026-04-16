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
        if row[loader.TYPE] != "Territory" or row[loader.NAME].startswith("*"):
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
