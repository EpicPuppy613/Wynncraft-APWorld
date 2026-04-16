from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .data import loader

if TYPE_CHECKING:
    from .world import WynncraftWorld

item_names = []
filler_names = []
trap_names = []
item_name_to_id = {}
default_item_classifications = {}

for row in loader.rows:
    if not row[loader.AP] in ["Item", "Filler", "Trap"] or row[loader.ID] == '':
        continue
    item_id = int(row[loader.ID].replace(" ", ""), 16)
    name = row[loader.NAME]
    item_class = ItemClassification.filler
    match row[loader.TYPE]:
        case "Territory":
            name = "Region: " + name
            item_class |= ItemClassification.progression
        case "Special":
            item_class |= ItemClassification.progression
            if name.startswith("Max Level"):
                item_class |= ItemClassification.useful
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

class WynncraftItem(Item):
    game = "Wyncraft"

def get_random_filler_item_name(world: WynncraftWorld) -> str:
    return filler_names[world.random.randint(0, len(filler_names) - 1)]


def create_item_with_correct_classification(world: WynncraftWorld, name: str) -> WynncraftItem:
    classification = default_item_classifications[name]
    return WynncraftItem(name, classification, item_name_to_id[name], world.player)


def create_all_items(world: WynncraftWorld) -> None:
    itempool: list[Item] = []

    for item in item_names:
        ap_item = world.create_item(item)
        itempool.append(ap_item)
        if item == "Region: Ragni Main Entrance" or item == "Region: Emerald Trail":
            world.push_precollected(ap_item)

    level_items = 3
    for i in range(level_items):
        itempool.append(world.create_item("Progressive Max Level"))

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += itempool
