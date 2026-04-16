from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups, option_presets


class WynncraftWebWorld(WebWorld):
    game = "Wynncraft"

    theme = "grassFlowers"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Wynncraft for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["EpicPuppy613"],
    )

    tutorials = [setup_en]

    option_groups = option_groups
    options_presets = option_presets
