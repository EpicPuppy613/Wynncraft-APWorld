from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, Range, Choice, Toggle


class GoalLevel(Range):
    """
    Level to reach to win the game.
    """

    display_name = "Goal Level"

    range_start = 10
    range_end = 60
    default = 40

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
    None: Only Ragni starts unlocked (may lead to fill errors)
    Alekin: The route from Ragni -> Alekin starts unlocked
    Hybrid: Same as Alekin option and the rest of the route to Detlas is guaranteed to be in sphere 1
    Detlas: The route from Ragni -> Detlas starts unlocked
    """

    display_name = "Starting Route"

    option_none = 0
    option_alekin = 1
    option_hybrid = 2
    option_detlas = 3

    default = 2

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
    default = 10

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
    Earn checks for entering territories for the first time.
    Disabling this removes a lot of checks.
    """

    display_name = "Territorysanity"

    default = True

@dataclass
class WynncraftOptions(PerGameCommonOptions):
    goal_level: GoalLevel
    locked_region_enforcement: LockedRegionEnforcement
    locked_region_countdown: LockedRegionCountdown

    starting_route: StartingRoute
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

    trap_chance: TrapChance
    freeze_trap_weight: FreezeTrapWeight
    daze_trap_weight: DazeTrapWeight
    blind_trap_weight: BlindTrapWeight
    kill_trap_weight: KillTrapWeight
    trap_duration: TrapDuration


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [GoalLevel, LockedRegionEnforcement, LockedRegionCountdown],
    ),
    OptionGroup(
        "Item Options",
        [StartingRoute, LevelIncrement, ExtraMaxLevels, GearLockMode, SingleGearRarity, GearLevelIncrement, ExtraGearLevels]
    ),
    OptionGroup(
        "Location Options",
        [QuestChecks, MiniQuestChecks, CaveChecks, DungeonChecks, LevelChecks, TerritoryChecks]
    ),
    OptionGroup(
        "Trap Options",
        [TrapChance, FreezeTrapWeight, DazeTrapWeight, BlindTrapWeight, KillTrapWeight, TrapDuration]
    )
]

option_presets = {}
