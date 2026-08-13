from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from Options import OptionError

from .data import loader

if TYPE_CHECKING:
    from .world import WynncraftWorld

item_names = []
filler_names = []
trap_names = []
item_name_to_id = {}
default_item_classifications = {}
item_levels = {}

ALEKIN_ROUTE = [
    "Region: Ragni Main Entrance",
    "Region: Emerald Trail",
    "Region: Entrance to Nivla Woods",
    "Region: Nivla Woods"
]

DETLAS_ROUTE = [
    "Region: Road to Time Valley",
    "Region: Nivla Woods Exit",
    "Region: Akias Ruins",
    "Region: Corrupted Orchard",
    "Region: Detlas Suburbs"
]

for row in loader.rows:
    if not row[loader.AP] in ["Item", "Filler", "Trap"] or row[loader.ID] == "":
        continue
    item_id = int(row[loader.ID].replace(" ", ""), 16)
    name = row[loader.NAME]
    item_class = ItemClassification.filler
    if row[loader.TYPE] == "Region":
        name = "Region: " + name
        item_class |= ItemClassification.progression
    if name == "Progressive Max Level":
        item_class |= ItemClassification.progression
    elif name.startswith("Progressive"):
        item_class |= ItemClassification.progression
    match row[loader.AP]:
        case "Item":
            item_names.append(name)
        case "Filler":
            filler_names.append(name)
        case "Trap":
            item_class |= ItemClassification.trap
            trap_names.append(name)

    item_name_to_id[name] = item_id
    default_item_classifications[name] = item_class

    if row[loader.LEVEL] == "" or row[loader.TYPE] == "Special":
        continue
    item_levels[name] = int(row[loader.LEVEL])

class WynncraftItem(Item):
    game = "Wynncraft"

def get_random_filler_item_name(world: WynncraftWorld) -> str:
    return filler_names[world.random.randint(0, len(filler_names) - 1)]

def create_item_with_correct_classification(world: WynncraftWorld, name: str) -> WynncraftItem:
    classification = default_item_classifications[name]
    return WynncraftItem(name, classification, item_name_to_id[name], world.player)

def get_trap_weight(world: WynncraftWorld, trap: str):
    match trap:
        case "Freeze Trap":
            return world.options.freeze_trap_weight
        case "Silence Trap":
            return world.options.daze_trap_weight
        case "Blind Trap":
            return world.options.blind_trap_weight
        case "Kill Trap":
            return world.options.kill_trap_weight
    return 0


def create_all_items(world: WynncraftWorld) -> None:
    starting_route = world.options.starting_route
    starting_items = []
    if starting_route in [starting_route.option_alekin, starting_route.option_detlas]:
        starting_items += ALEKIN_ROUTE
    if starting_route == starting_route.option_detlas:
        starting_items += DETLAS_ROUTE

    itempool: list[Item] = []

    for item, level in item_levels.items():
        if level > world.max_level:
            continue

        ap_item = world.create_item(item)
        if item in starting_items:
            world.push_precollected(ap_item)
        else:
            itempool.append(ap_item)

    level_items = ceil(world.max_level / world.options.level_increment)
    itempool += [world.create_item("Progressive Max Level") for _ in range(level_items)]

    gear_types = []
    gear_items = []

    if world.options.gear_lock_mode == world.options.gear_lock_mode.option_full:
        gear_types += ["Armor", "Accessories", "Weapons"]
    elif world.options.gear_lock_mode == world.options.gear_lock_mode.option_unified:
        gear_types += ["Gear"]

    if len(gear_types) > 0:
        gear_item_count = ceil(world.max_level / world.options.gear_level_increment)
        if not world.options.single_gear_rarity:
            for gear in gear_types:
                itempool += [world.create_item("Progressive Unique " + gear) for _ in range(gear_item_count)]
                itempool += [world.create_item("Progressive Rare " + gear) for _ in range(gear_item_count)]
                itempool += [world.create_item("Progressive Legendary+ " + gear) for _ in range(gear_item_count)]
                gear_items += ["Progressive Unique " + gear, "Progressive Rare " + gear, "Progressive Legendary+ " + gear]
        else:
            for gear in gear_types:
                itempool += [world.create_item("Progressive " + gear) for _ in range(gear_item_count)]
                gear_items += ["Progressive " + gear]

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    if needed_number_of_filler_items < 0:
        raise OptionError("Not enough checks. Please enabled additional sanities or increase level increments.")

    extra_level_items = min(world.options.extra_max_levels, needed_number_of_filler_items)
    itempool += [world.create_item("Progressive Max Level") for _ in range(extra_level_items)]
    needed_number_of_filler_items -= extra_level_items

    extra_gear_items = min(world.options.extra_gear_levels * len(gear_items), needed_number_of_filler_items)
    for i in range(extra_gear_items):
        index = i % len(gear_items)
        itempool += [world.create_item(gear_items[index])]
    needed_number_of_filler_items -= extra_gear_items

    trap_items = round(needed_number_of_filler_items * world.options.trap_chance / 100)

    total_trap_weight = 0
    for trap in trap_names:
        total_trap_weight += get_trap_weight(world, trap)

    if total_trap_weight != 0:
        for i in range(trap_items):
            roll = world.random.randint(0, total_trap_weight - 1)
            for trap in trap_names:
                weight = get_trap_weight(world, trap)
                if roll < weight:
                    itempool.append(world.create_item(trap))
                    break
                roll -= get_trap_weight(world, trap)
        needed_number_of_filler_items -= trap_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += itempool
