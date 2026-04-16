from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, Range

class TrapChance(Range):
    """
    Percentage chance that any given filler item will be replaced by a random trap.
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0


@dataclass
class WynncraftOptions(PerGameCommonOptions):
    trap_chance: TrapChance


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [TrapChance],
    ),
]

option_presets = {
    "default": {
        "trap_chance": 0,
    }
}
