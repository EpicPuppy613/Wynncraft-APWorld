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

        if int(row[loader.LEVEL]) > world.max_level:
            continue

        regions.append(Region(row[loader.NAME], world.player, world.multiworld))
        world.all_regions.append(row[loader.NAME])

        if row[loader.AP] == "Item":
            world.unlockable_regions.append(row[loader.NAME])

    for i in range(1, world.max_level + 1):
        regions.append(Region("Level " + str(i), world.player, world.multiworld))

    for i in range(1, world.max_level + 1):
        regions.append(Region("Gear Level " + str(i) + " Access", world.player, world.multiworld))

    if world.is_level_goal:
        regions.append(Region("Level " + str(world.options.goal_level), world.player, world.multiworld))

    world.multiworld.regions += regions


def connect_regions(world: WynncraftWorld) -> None:
    for row in loader.rows:
        if row[loader.TYPE] != "Region" or row[loader.NAME].startswith("*"):
            continue
        if int(row[loader.LEVEL]) > world.max_level:
            continue
        if row[loader.CONNECTIONS] == "":
            continue

        region = world.get_region(row[loader.NAME])
        for connection in row[loader.CONNECTIONS].split(", "):
            if connection in world.all_regions:
                region.connect(world.get_region(connection), f"{row[loader.NAME]} to {connection}")

    for i in range(2, world.max_level + 1):
        curr_level = world.get_region("Level " + str(i))
        prev_level = world.get_region("Level " + str(i - 1))
        prev_level.connect(curr_level, f"Level Up: " + str(i))

        curr_gear_level = world.get_region("Gear Level " + str(i) + " Access")
        prev_gear_level = world.get_region("Gear Level " + str(i) + " Access")
        prev_gear_level.connect(curr_gear_level, f"Gear Level Cap: " + str(i))

    if world.is_level_goal:
        curr_level = world.get_region("Level " + str(world.options.goal_level))
        prev_level = world.get_region("Level " + str(world.options.goal_level - 1))
        prev_level.connect(curr_level, f"Level Up: " + str(world.options.goal_level))

    # Connection from default region to starting region in game (Ragni)
    world.get_region("Menu").connect(world.get_region("Ragni"), "Menu to Ragni")

    world.get_region("Menu").connect(world.get_region("Level 1"), "Level Up: 1")
    world.get_region("Menu").connect(world.get_region("Gear Level 1 Access"), "Gear Level Cap: 1")
