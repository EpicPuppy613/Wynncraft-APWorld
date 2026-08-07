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

    for region in loader.all_regions:
        if region.startswith("*"):
            continue
        regions.append(Region(region, world.player, world.multiworld))

    world.multiworld.regions += regions


def connect_regions(world: WynncraftWorld) -> None:
    for name in loader.all_regions:
        if loader.region_connections[name] == "":
            continue
        region = world.get_region(name)
        for connection in loader.region_connections[name].split(", "):
            region.connect(world.get_region(connection), f"{name} to {connection}")

    # Connection from default region to starting region in game (Ragni)
    world.get_region("Menu").connect(world.get_region("Ragni"), "Menu to Ragni")
