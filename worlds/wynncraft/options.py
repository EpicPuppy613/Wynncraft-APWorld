from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md


# The first type of Option we'll discuss is the Toggle.
# A toggle is an option that can either be on or off. This will be represented by a checkbox on the website.
# The default for a toggle is "off".
# If you want a toggle to be on by default, you can use the "DefaultOnToggle" class instead of the "Toggle" class.
'''
class HardMode(Toggle):
    """
    In hard mode, the basic enemy and the final boss will have more health.
    The Health Upgrades become progression, as they are now required to beat the final boss.
    """

    # The docstring of an option is used as the description on the website and in the template yaml.

    # You'll also want to set a display name, which will determine what the option is called on the website.
    display_name = "Hard Mode"


class Hammer(Toggle):
    """
    Adds another item to the itempool: The Hammer.
    The top middle chest will now be locked behind a breakable wall, requiring the Hammer.
    """

    display_name = "Hammer"


class ExtraStartingChest(Toggle):
    """
    Adds an extra chest in the bottom left, making room for an extra Confetti Cannon.
    """

    display_name = "Extra Starting Chest"
'''

class TrapChance(Range):
    """
    Percentage chance that any given filler item will be replaced by a random trap.
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0

'''
class StartWithOneConfettiCannon(Toggle):
    """
    Start with a confetti cannon already in your inventory.
    Why? Because you deserve it. You get to celebrate yourself without doing any work first.
    """

    display_name = "Start With One Confetti Cannon"


# A Range is a numeric option with a min and max value. This will be represented by a slider on the website.
class ConfettiExplosiveness(Range):
    """
    How much confetti each use of a confetti cannon will fire.
    """

    display_name = "Confetti Explosiveness"

    range_start = 0
    range_end = 10

    # Range options must define an explicit default value.
    default = 3


# A Choice is an option with multiple discrete choices. This will be represented by a dropdown on the website.
class PlayerSprite(Choice):
    """
    The sprite that the player will have.
    """

    display_name = "Player Sprite"

    option_human = 0
    option_duck = 1
    option_horse = 2
    option_cat = 3

    # Choice options must define an explicit default value.
    default = option_human

    # For choices, you can also define aliases.
    # For example, we could make it so "player_sprite: kitty" resolves to "player_sprite: cat" like this:
    alias_kitty = option_cat
'''

# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class WynncraftOptions(PerGameCommonOptions):
    trap_chance: TrapChance


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Gameplay Options",
        [TrapChance],
    ),
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    "default": {
        "trap_chance": 0,
    }
}
