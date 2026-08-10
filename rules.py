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


def set_all_location_rules(world: WynncraftWorld) -> None:
    for row in loader.rows:
        if row[loader.AP] != "Location" or row[loader.LEVEL] == "" or int(row[loader.LEVEL]) >= world.options.goal_level:
            continue

        if not world.location_enabled(row[loader.TYPE]):
            continue

        regions = row[loader.REGION].split(", ")

        if row[loader.TYPE] == "Level":
            rule = True_()
            try:
                prev_level = int(row[loader.NAME].replace("Level Up: ", "")) - 1
                if prev_level > 1:
                    rule &= CanReachLocation("Level Up: " + str(prev_level))
            except ValueError:
                pass
            world.get_location(row[loader.NAME]).item_rule = lambda item: item.name != "Progressive Max Level"
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

        levels_needed = max_levels_needed(int(row[loader.LEVEL]), world)
        world.set_rule(world.get_location(row[loader.NAME]), Has("Progressive Max Level", count=levels_needed) & rule)

    # Victory condition
    world.set_rule(world.get_location("Level Up: " + str(world.options.goal_level)),
                   Has("Progressive Max Level", count=max_levels_needed(world.options.goal_level.value, world)))


def set_completion_condition(world: WynncraftWorld) -> None:
    world.set_completion_rule(Has("Victory"))

def max_levels_needed(level: int, world: WynncraftWorld):
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
