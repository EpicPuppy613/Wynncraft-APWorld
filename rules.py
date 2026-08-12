from __future__ import annotations

from typing import TYPE_CHECKING

from math import ceil

from rule_builder.rules import Has, True_, False_, CanReachRegion, CanReachLocation, Rule

from .data import loader

if TYPE_CHECKING:
    from .world import WynncraftWorld


def set_all_rules(world: WynncraftWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: WynncraftWorld) -> None:
    for row in loader.rows:
        if row[loader.TYPE] != "Region" or row[loader.NAME].startswith("*"):
            continue
        if int(row[loader.LEVEL]) >= world.options.goal_level:
            continue
        if row[loader.CONNECTIONS] == "":
            continue

        for connection in row[loader.CONNECTIONS].split(", "):
            if connection in world.unlockable_regions:
                entrance = world.get_entrance(f"{row[loader.NAME]} to {connection}")
                world.set_rule(entrance, Has(f"Region: {connection}"))

    for i in range(2, world.options.goal_level + 1):
        entrance = world.get_entrance(f"Level Up: " + str(i))
        if str(i) in loader.level_map and world.options.logical_levels:
            rule = False_()
            for region in loader.level_map[str(i)].split(", "):
                rule = rule | CanReachRegion(region)
        else:
            rule = True_()
        world.set_rule(entrance, rule & Has("Progressive Max Level", count=max_levels_needed(i, world)))


def set_all_location_rules(world: WynncraftWorld) -> None:
    for row in loader.rows:
        if row[loader.AP] != "Location" or row[loader.LEVEL] == "" or int(row[loader.LEVEL]) >= world.options.goal_level:
            continue

        if not world.location_enabled(row[loader.TYPE]) and row[loader.IS_PREREQ] == "FALSE":
            continue

        regions = row[loader.REGION].split(", ")

        if row[loader.TYPE] == "Level":
            world.get_location(row[loader.NAME]).item_rule = lambda item: item.name != "Progressive Max Level"
            continue
        else:
            rule = True_()
            if len(regions) > 1:
                del regions[0]
                for region in regions:
                    if region.startswith("*"):
                        rule = rule & Has(f"Region: {region[1:]}")
                    else:
                        rule = rule & CanReachRegion(region)

            if row[loader.PREREQUISITES] != "":
                prereqs = row[loader.PREREQUISITES].split(", ")
                for prereq in prereqs:
                    rule = rule & CanReachLocation(prereq)

            if row[loader.GEAR_REQ] != "":
                gear_reqs = row[loader.GEAR_REQ].split(", ")
                for req in gear_reqs:
                    rule = rule & gear_rule(world, req)

        if row[loader.TYPE] == "Territory":
            world.set_rule(world.get_location(row[loader.NAME]), CanReachRegion("Level " + str(max(1,int(row[loader.LEVEL]) - world.options.early_territory_levels))) & rule)
        else:
            world.set_rule(world.get_location(row[loader.NAME]), CanReachRegion("Level " + row[loader.LEVEL]) & rule)


def set_completion_condition(world: WynncraftWorld) -> None:
    world.set_completion_rule(Has("Victory"))

def max_levels_needed(level: int, world: WynncraftWorld):
    if level <= 0:
        return 0
    return ceil((level - 1) / world.options.level_increment)

def gear_levels_needed(level: int, world: WynncraftWorld):
    return ceil((level - 1) / world.options.gear_level_increment)

def gear_rule(world: WynncraftWorld, requirement: str) -> Rule:
    if world.options.gear_lock_mode == world.options.gear_lock_mode.option_off:
        return True_()
    parts = requirement.split(" ")
    if world.options.gear_lock_mode == world.options.gear_lock_mode.option_unified:
        parts[1] = "Gear"
    if world.options.single_gear_rarity:
        return Has("Progressive " + parts[1], count=int(gear_levels_needed(int(parts[2]), world)))
    else:
        return Has("Progressive " + parts[0] + " " + parts[1], count=int(gear_levels_needed(int(parts[2]), world)))
