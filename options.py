from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, Range, Choice, Toggle, TextChoice


class GoalType(Choice):
    """
    Level: Reach the target level
    Dungeon: Complete the specified dungeon
    Quest: Complete the specified quest
    """

    display_name = "Objective"

    option_level = 0
    option_dungeon = 1
    option_quest = 2

    default = 0

class GoalLevel(Range):
    """
    'Level' objective only:
    The level to reach to win the game.
    """

    display_name = "Goal Level"

    range_start = 10
    range_end = 120
    default = 40

default_dungeon_map = {
    0: "Infested Pit",
    1: "Underworld Crypt",
    2: "Timelost Sanctum",
    3: "Sand-Swept Tomb",
    4: "Ice Barrows",
    5: "Undergrowth Ruins",
    6: "Galleon's Graveyard",
    7: "Corrupted Lost Sanctuary",
    8: "Fallen Factory",
    9: "Eldrich Outlook"
}

class GoalDungeon(TextChoice):
    """
    'Dungeon' objective only:
    The dungeon to beat to win the game.
    Can be set to any dungeon in the game.
    """

    display_name = "Goal Dungeon"

    option_pit = 0
    option_crypt = 1
    option_sanctum = 2
    option_tomb = 3
    option_barrows = 4
    option_ruins = 5
    option_graveyard = 6
    option_corrupt_sanctuary = 7
    option_factory = 8
    option_outlook = 9

    default = option_tomb

    @classmethod
    def get_option_name(cls, value: str | int) -> str:
        if isinstance(value, str):
            return value
        if value in default_dungeon_map:
            return default_dungeon_map[value]
        else:
            return ""

default_quest_map = {
    0: "Arachnid's Ascent",
    1: "Kingdom of Sand",
    2: "Heart of Llevigar",
    3: "Jungle Fever",
    4: "The Worm Holes",
    5: "Redbeard's Booty",
    6: "WynnExcavation Site D",
    7: "Reincarnation",
    8: "Tower of Ascension",
    9: "The Realm of Light",
    10: "The Feathers Fly Part II",
    11: "The Breaking Point",
    12: "A Hunter's Calling",
    13: "Apotheosis"
}

class GoalQuest(TextChoice):
    """
    'Quest' objective only:
    The quest to complete to win the game.
    Can be set to any quest in the game.
    """

    display_name = "Goal Quest"

    option_arachnid = 0
    option_sand = 1
    option_llevigar = 2
    option_jungle = 3
    option_worm = 4
    option_redbeard = 5
    option_excavation = 6
    option_reincarnation = 7
    option_ascension = 8
    option_light = 9
    option_feathers = 10
    option_breaking = 11
    option_hunters = 12
    option_apotheosis =13

    default = option_llevigar

    @classmethod
    def get_option_name(cls, value: str | int) -> str:
        if isinstance(value, str):
            return value
        if value in default_quest_map:
            return default_quest_map[value]
        else:
            return ""

class ExtraMaxLevels(Range):
    """
    Number of filler items to convert to extra max level items.
    This should make it easier to get all max levels needed to win, as well as reducing how much you get stuck.
    Not all of these are guaranteed to be added, depending on item and location counts during generation.
    """

    display_name = "Extra Level Items"

    range_start = 0
    range_end = 50
    default = 5

class StartingRoute(Choice):
    """
    How much of the route from Ragni to Detlas to start unlocked
    None: WARNING - May cause generation errors
    Alekin: Ragni -> Alekin
    Detlas: Ragni -> Detlas
    """

    display_name = "Starting Route"

    option_none = 0
    option_alekin = 1
    option_detlas = 2

    default = 1

class LevelIncrement(Range):
    """
    How many levels each max level item increases by.
    Set this higher if you disable a lot of checks.
    """

    display_name = "Level Increment"

    range_start = 1
    range_end = 10
    default = 1

class GearLockMode(Choice):
    """
    Prevent gear from being used until it is unlocked
    Full: Armor, Accessories, and Weapons are unlocked independently
    Unified: All gear types are unlocked with a single item
    """

    display_name = "Gear Lock"

    option_full = 0
    option_unified = 1
    option_off = 2

    default = option_unified

class SingleGearRarity(Toggle):
    """
    Whether to combine all gear rarities (unique, rare, legendary+) into a single progressive level
    """

    display_name = "Single Gear Rarity"

    default = False

class GearLevelIncrement(Range):
    """
    How much to increase max gear level each item
    """

    display_name = "Gear Level Increment"

    range_start = 1
    range_end = 20
    default = 5

class ExtraGearLevels(Range):
    """
    Number of filler items to convert to extra max gear level items per gear type (armor, accessories, weapons).
    Not all of these are guaranteed to be added, depending on item and location counts during generation.
    """

    display_name = "Extra Gear Level Items"

    range_start = 0
    range_end = 50
    default = 3

class TrapChance(Range):
    """
    Percent of 'Nothing' filler items to replace with traps.
    """

    display_name = "Trap Percent"

    range_start = 0
    range_end = 100
    default = 50

class FreezeTrapWeight(Range):
    """
    Relative weight of freeze traps.
    Freeze trap: Freezes player movement.
    """

    display_name = "Freeze Trap Weight"

    range_start = 0
    range_end = 100
    default = 3

class DazeTrapWeight(Range):
    """
    Relative weight of daze traps.
    Daze trap: Disables player attacks/spells.
    """

    display_name = "Daze Trap Weight"

    range_start = 0
    range_end = 100
    default = 3

class BlindTrapWeight(Range):
    """
    Relative weight of blind traps.
    Blind trap: Blacks out the entire screen.
    """

    display_name = "Blind Trap Weight"

    range_start = 0
    range_end = 100
    default = 3

class KillTrapWeight(Range):
    """
    Relative weight of kill traps.
    Kill trap: Immediately kills the player.
    """

    display_name = "Kill Trap Weight"

    range_start = 0
    range_end = 100
    default = 1

class TrapDuration(Range):
    """
    Number of seconds for freeze, daze, and blind traps to take effect.
    """

    display_name = "Trap Duration"

    range_start = 1
    range_end = 120
    default = 15

class LockedRegionEnforcement(Choice):
    """
    Kill: Run /kill upon entering any locked region.
    Countdown: Run /kill after being in a locked region for a certain amount of time.
    Lenient: No locked region enforcement.
    """

    display_name = "Locked Region Enforcement"

    option_kill = 0
    option_countdown = 1
    option_lenient = 2

    default = option_countdown

class LockedRegionCountdown(Range):
    """
    When using 'Countdown' enforcement, the number of seconds in a locked region until /kill is run.
    """

    display_name = "Locked Region Countdown"

    range_start = 1
    range_end = 60
    default = 3

class QuestChecks(Toggle):
    """
    Earn checks for completing quests.
    Disabling this removes a lot of checks.
    """

    display_name = "Questsanity"

    default = True

class MiniQuestChecks(Toggle):
    """
    Earn checks for completing mini-quests.
    Disabling this removes some checks.
    """

    display_name = "Mini-Questsanity"

    default = True

class CaveChecks(Toggle):
    """
    Earn checks for completing caves.
    Disabling this removes a lot of checks.
    """

    display_name = "Cavesanity"

    default = True

class DungeonChecks(Toggle):
    """
    Earn checks for completing dungeons.
    Disabling this removes some checks.
    """

    display_name = "Dungeonsanity"

    default = True

class LevelChecks(Toggle):
    """
    Earn checks for leveling up.
    Disabling this removes a lot of checks.
    """

    display_name = "Levelsanity"

    default = True

class TerritoryChecks(Toggle):
    """
    Earn checks for visiting territories for the first time.
    Disabling this removes a lot of checks.
    """

    display_name = "Territorysanity"

    default = True

class EarlyTerritoryLevels(Range):
    """
    How many levels below the territory's recommended level
    needed for Territorysanity checks to be considered in-logic.
    """

    display_name = "Early Territory Access"

    range_start = 0
    range_end = 20
    default = 5


class LogicalLevels(Toggle):
    """
    Whether level-based checks should require
    having access to later-game areas.
    Disabling this could lead to a very grindy early game.
    """

    display_name = "Logical Levels"

    default = True

class LogicalGearLevels(Toggle):
    """
    Whether level-based checks should require
    a minimum level of gear.
    Disabling this could lead to being underpowered throughout the game.
    """

    display_name = "Logical Gear Levels"

    default = True

class DeathLink(Toggle):
    """
    Enable death link.
    """

    display_name = "Death Link"

    default = False

@dataclass
class WynncraftOptions(PerGameCommonOptions):
    goal_type: GoalType
    goal_level: GoalLevel
    goal_dungeon: GoalDungeon
    goal_quest: GoalQuest

    starting_route: StartingRoute
    locked_region_enforcement: LockedRegionEnforcement
    locked_region_countdown: LockedRegionCountdown

    level_increment: LevelIncrement
    extra_max_levels: ExtraMaxLevels
    gear_lock_mode: GearLockMode
    single_gear_rarity: SingleGearRarity
    gear_level_increment: GearLevelIncrement
    extra_gear_levels: ExtraGearLevels

    quest_checks: QuestChecks
    mini_quest_checks: MiniQuestChecks
    cave_checks: CaveChecks
    dungeon_checks: DungeonChecks
    level_checks: LevelChecks
    territory_checks: TerritoryChecks
    early_territory_levels: EarlyTerritoryLevels
    logical_levels: LogicalLevels
    logical_gear_levels: LogicalGearLevels

    trap_chance: TrapChance
    freeze_trap_weight: FreezeTrapWeight
    daze_trap_weight: DazeTrapWeight
    blind_trap_weight: BlindTrapWeight
    kill_trap_weight: KillTrapWeight
    trap_duration: TrapDuration

    death_link: DeathLink


option_groups = [
    OptionGroup(
        "Goal Options",
        [GoalType, GoalLevel, GoalDungeon, GoalQuest]
    ),
    OptionGroup(
        "Region Lock Options",
        [StartingRoute, LockedRegionEnforcement, LockedRegionCountdown],
    ),
    OptionGroup(
        "Item Options",
        [LevelIncrement, ExtraMaxLevels, GearLockMode, SingleGearRarity, GearLevelIncrement, ExtraGearLevels]
    ),
    OptionGroup(
        "Location Options",
        [QuestChecks, MiniQuestChecks, CaveChecks, DungeonChecks, LevelChecks, TerritoryChecks, EarlyTerritoryLevels, LogicalLevels, LogicalGearLevels]
    ),
    OptionGroup(
        "Trap Options",
        [TrapChance, FreezeTrapWeight, DazeTrapWeight, BlindTrapWeight, KillTrapWeight, TrapDuration]
    ),
    OptionGroup(
        "Miscellaneous Options",
        [DeathLink]
    )
]

option_presets = {}
