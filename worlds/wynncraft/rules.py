from __future__ import annotations

from typing import TYPE_CHECKING

from math import ceil

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

from .data import loader

if TYPE_CHECKING:
    from .world import APQuestWorld


def set_all_rules(world: APQuestWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: APQuestWorld) -> None:
    for row in loader.rows:
        if row[loader.TYPE] != "Territory" or row[loader.CONNECTIONS] == "":
            continue
        for connection in row[loader.CONNECTIONS].split(", "):
            entrance = world.get_entrance(f"{row[loader.NAME]} to {connection}")
            if connection in loader.unlockable_regions:
                set_rule(entrance, lambda state: state.has(f"Region: {connection}", world.player))


def set_all_location_rules(world: APQuestWorld) -> None:
    for row in loader.rows:
        if row[loader.AP] != "Location" or int(row[loader.LEVEL]) == 1:
            continue

        levels_needed = ceil(int(row[loader.LEVEL]) / 5)
        set_rule(world.get_location(row[loader.NAME]), lambda state: state.has("Progressive Max Level", world.player, levels_needed))
    # Location rules work no differently from Entrance rules.
    # Most of our locations are chests that can simply be opened by walking up to them.
    # Thus, their logical requirements are covered by the Entrance rules of the Entrances that were required to
    # reach the region that the chest sits in.
    # However, our two enemies work differently.
    # Entering the room with the enemy is not enough, you also need to have enough combat items to be able to defeat it.
    # So, we need to set requirements on the Locations themselves.
    # Since combat is a bit more complicated, we'll use this chance to cover some advanced access rule concepts.

    # Sometimes, you may want to have different rules depending on the player's chosen options.
    # There is a wrong way to do this, and a right way to do this. Let's do the wrong way first.
    '''
    right_room_enemy = world.get_location("Right Room Enemy Drop")

    # DON'T DO THIS!!!!
    set_rule(
        right_room_enemy,
        lambda state: (
            state.has("Sword", world.player)
            and (not world.options.hard_mode or state.has_any(("Shield", "Health Upgrade"), world.player))
        ),
    )
    # DON'T DO THIS!!!!

    # Now, what's actually wrong with this? It works perfectly fine, right?
    # If hard mode disabled, Sword is enough. If hard mode is enabled, we also need a Shield or a Health Upgrade.
    # The access rule we just wrote does this correctly, so what's the problem?
    # The problem is performance.
    # Most of your world code doesn't need to be perfectly performant, since it just runs once per slot.
    # However, access rules in particular are by far the hottest code path in Archipelago.
    # An access rule will potentially be called thousands or even millions of times over the course of one generation.
    # As a result, access rules are the one place where it's really worth putting in some effort to optimize.
    # What's the performance problem here?
    # Every time our access rule is called, it has to evaluate whether world.options.hard_mode is True or False.
    # Wouldn't it be better if in easy mode, the access rule only checked for Sword to begin with?
    # Wouldn't it also be better if in hard mode, it already knew it had to check Shield and Health Upgrade as well?
    # Well, we can achieve this by doing the "if world.options.hard_mode" check outside the set_rule call,
    # and instead having two *different* set_rule calls depending on which case we're in.

    if world.options.hard_mode:
        # If you have multiple conditions, you can obviously chain them via "or" or "and".
        # However, there are also the nice helper functions "state.has_any" and "state.has_all".
        set_rule(
            right_room_enemy,
            lambda state: (
                state.has("Sword", world.player) and state.has_any(("Shield", "Health Upgrade"), world.player)
            ),
        )
    else:
        set_rule(right_room_enemy, lambda state: state.has("Sword", world.player))

    # Another way to chain multiple conditions is via the add_rule function.
    # This makes the access rules a bit slower though, so it should only be used if your structure justifies it.
    # In our case, it's pretty useful because hard mode and easy mode have different requirements.
    final_boss = world.get_location("Final Boss Defeated")

    # For the "known" requirements, it's still better to chain them using a normal "and" condition.
    add_rule(final_boss, lambda state: state.has_all(("Sword", "Shield"), world.player))

    if world.options.hard_mode:
        # You can check for multiple copies of an item by using the optional count parameter of state.has().
        add_rule(final_boss, lambda state: state.has("Health Upgrade", world.player, 2))
    '''


def set_completion_condition(world: APQuestWorld) -> None:
    # Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
    # You can just set a completion condition directly like any other condition, referencing items the player receives:
    # world.multiworld.completion_condition[world.player] = lambda state: state.has_all(("Sword", "Shield"), world.player)

    # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    # So lets undo what we just did, and instead set the completion condition to:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
