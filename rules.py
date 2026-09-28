from __future__ import annotations

from typing import TYPE_CHECKING

from math import ceil

from rule_builder.rules import Has, True_, False_, CanReachRegion, CanReachLocation, Rule

from .data import loader

if TYPE_CHECKING:
    from .world import WynncraftWorld


def set_all_rules(world: WynncraftWorld) -> None:
    set_all_entrance_rules(world)
    set_all_level_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: WynncraftWorld) -> None:
    conn_rules = {}

    for conn_row in loader.conn_rows:
        if int(conn_row[loader.LEVEL]) > world.max_level:
            continue
        conn_from = conn_row[loader.CONN_FROM]
        if not conn_from in conn_rules:
            conn_rules[conn_from] = {}
        conn_rules[conn_from][conn_row[loader.CONN_TO]] = conn_row[loader.PREREQS]

    for row in loader.rows:
        if row[loader.TYPE] != "Region":
            continue
        if int(row[loader.LEVEL]) > world.max_level:
            continue
        if len(row[loader.CONNECTIONS]) == 0:
            continue

        for connection in row[loader.CONNECTIONS]:
            if connection in world.unlockable_regions:
                entrance = world.get_entrance(f"{row[loader.NAME]} to {connection}")

                conn_rule = True_()
                if row[loader.NAME] in conn_rules and connection in conn_rules[row[loader.NAME]]:
                    conn_rule = True_()
                    for location in conn_rules[row[loader.NAME]][connection]:
                        conn_rule = conn_rule & CanReachLocation(location)

                world.set_rule(entrance, Has(f"Region: {connection}") & Has(
                    "Level " + str(max(1, int(row[loader.LEVEL]) - world.options.early_territory_levels.value))) & conn_rule)


def set_all_level_rules(world: WynncraftWorld) -> None:
    def set_level_logic(level: int) -> None:
        rule = Has("Level " + str(level - 1))

        for rule_row in loader.level_rows:
            if int(rule_row[loader.LEVEL]) != level or not world.level_rule_enabled(rule_row[loader.TYPE]):
                continue

            sub_rule = False_()
            for region in rule_row[loader.LVL_REGIONS]:
                sub_rule = sub_rule | CanReachRegion(region)

            for location in rule_row[loader.PREREQS]:
                sub_rule = sub_rule | CanReachLocation(location)

            rule = rule & sub_rule

        if (level - 1) % 5 == 0:
            rule = rule & Has("Gear Level " + str(level) + " Access")

        world.set_rule(world.get_location("Level Cap: " + str(level)), rule & Has("Progressive Max Level", count=max_levels_needed(level, world)))

    for i in range(2, world.max_level + 1):
        set_level_logic(i)
        if world.options.logical_gear_levels.value:
            gear_level_entrance = world.get_location("Gear Level Cap: " + str(i))
            world.set_rule(gear_level_entrance, gear_access_rule(world, i))

    if world.is_level_goal:
        world.set_rule(world.get_location("Level Up: " + str(world.options.goal_level.value)),
                       Has("Progressive Max Level", count=max_levels_needed(int(world.options.goal_level.value), world)) &
                       Has("Level " + str(int(world.options.goal_level.value) - 1)))


def set_all_location_rules(world: WynncraftWorld) -> None:
    for row in loader.rows:
        if row[loader.AP] != "Location" or row[loader.LEVEL] == "" or int(row[loader.LEVEL]) > world.max_level:
            continue

        if (not world.location_enabled(row[loader.TYPE]) and row[loader.IS_PREREQ] == "FALSE" and not
        ((world.is_dungeon_goal and row[loader.NAME] == world.goal_dungeon) or
         (world.is_quest_goal and row[loader.NAME] == world.goal_quest))):
            continue

        regions = row[loader.REGION].copy()

        if row[loader.TYPE] == "Level":
            world.get_location(row[loader.NAME]).item_rule = lambda item: item.name != "Progressive Max Level"
            world.set_rule(world.get_location(row[loader.NAME]), Has("Level " + row[loader.LEVEL]))
            continue
        else:
            rule = True_()
            if len(regions) > 1:
                del regions[0]
                for region in regions:
                    rule = rule & CanReachRegion(region)

            for alt_region in row[loader.ALT_REGIONS]:
                rule = rule & Has("Region: " + alt_region)

            if row[loader.PREREQS] != "":
                for prereq in row[loader.PREREQS]:
                    rule = rule & CanReachLocation(prereq)

            if row[loader.GEAR_REQ] != "":
                gear_reqs = row[loader.GEAR_REQ].split(", ")
                for req in gear_reqs:
                    rule = rule & gear_rule(world, req)

        if row[loader.TYPE] == "Territory":
            world.set_rule(world.get_location(row[loader.NAME]), Has(
                "Level " + str(max(1, int(row[loader.LEVEL]) - world.options.early_territory_levels.value))) & rule)
        else:
            world.set_rule(world.get_location(row[loader.NAME]), Has("Level " + row[loader.LEVEL]) & rule)


def set_completion_condition(world: WynncraftWorld) -> None:
    world.set_completion_rule(Has("Victory"))


def max_levels_needed(level: int, world: WynncraftWorld):
    if level <= 0:
        return 0
    return ceil((level - 1) / world.options.level_increment.value)


def gear_levels_needed(level: int, world: WynncraftWorld):
    return ceil(level / world.options.gear_level_increment.value)


def gear_rule(world: WynncraftWorld, requirement: str) -> Rule:
    if world.options.gear_lock_mode.value == world.options.gear_lock_mode.option_off:
        return True_()
    parts = requirement.split(" ")
    if world.options.gear_lock_mode.value == world.options.gear_lock_mode.option_unified:
        parts[1] = "Gear"
    if world.options.single_gear_rarity.value:
        return Has("Progressive " + parts[1], count=int(gear_levels_needed(int(parts[2]), world)))
    else:
        return Has("Progressive " + parts[0] + " " + parts[1], count=int(gear_levels_needed(int(parts[2]), world)))

def gear_access_rule(world: WynncraftWorld, level: int) -> Rule:
    if world.options.gear_lock_mode.value == world.options.gear_lock_mode.option_off:
        return True_()

    gear_types = []
    if world.options.gear_lock_mode.value == world.options.gear_lock_mode.option_full:
        gear_types += ["Armor", "Weapons"]
    elif world.options.gear_lock_mode.value == world.options.gear_lock_mode.option_unified:
        gear_types += ["Gear"]

    rule = True_()
    levels_needed = int(gear_levels_needed(level, world))
    if not world.options.single_gear_rarity.value:
        for gear in gear_types:
            rule = rule & (
                    Has("Progressive Unique " + gear, count=levels_needed) |
                    Has("Progressive Rare " + gear, count=levels_needed) |
                    Has("Progressive Legendary+ " + gear, count=levels_needed)
            )
    else:
        for gear in gear_types:
            rule = rule & Has("Progressive " + gear, count=levels_needed)

    return rule
