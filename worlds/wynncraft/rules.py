from __future__ import annotations

from typing import TYPE_CHECKING

from math import ceil

from rule_builder.rules import Has, True_, CanReachRegion, Rule

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
                world.set_rule(entrance, Has(f"Region: {connection}"))


def set_all_location_rules(world: WynncraftWorld) -> None:
    for row in loader.rows:
        if row[loader.AP] != "Location":
            continue

        regions = row[loader.REGION].split(", ")

        region_rule = True_()
        if len(regions) > 1:
            del regions[0]
            for region in regions:
                if region.startswith("*"):
                    region_rule = region_rule & Has(f"Region: {region[1:]}")
                else:
                    region_rule = region_rule & CanReachRegion(region)

        levels_needed = ceil(int(row[loader.LEVEL]) / 5) - 1
        world.set_rule(world.get_location(row[loader.NAME]), Has("Progressive Max Level", count=levels_needed) & region_rule)

    # Victory condition
    world.set_rule(world.get_location("Level Up: 20"), Has("Progressive Max Level", count=3))


def set_completion_condition(world: WynncraftWorld) -> None:
    world.set_completion_rule(Has("Victory"))
