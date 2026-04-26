from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, Range, Choice, Toggle


class GoalLevel(Range):
    """
    Level to reach to win the game.
    """

    display_name = "Goal Level"

    range_start = 10
    range_end = 40
    default = 40

class ExtraMaxLevels(Range):
    """
    Number of filler items to convert to extra max level items.
    This should make it easier to get all max levels needed to win, as well as reducing how much you get stuck.
    Not all of these are guaranteed to be added, depending on item and location counts during generation.
    """

    display_name = "Extra Max Levels"

    range_start = 0
    range_end = 40
    default = 5

class LevelIncrement(Range):
    """
    How many levels each max level item increases by.
    Set this higher if you disable a lot of checks.
    """

    display_name = "Level Increment"

    range_start = 1
    range_end = 10
    default = 1

class TrapChance(Range):
    """
    Percent of 'Nothing' filler items to replace with traps.
    """

    display_name = "Trap Chance"

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
    default = 2

class SilenceTrapWeight(Range):
    """
    Relative weight of silence traps.
    Silence trap: Disables player attacks/spells.
    """

    display_name = "Silence Trap Weight"

    range_start = 0
    range_end = 100
    default = 2

class BlindTrapWeight(Range):
    """
    Relative weight of blind traps.
    Blind trap: Blacks out the entire screen.
    """

    display_name = "Blind Trap Weight"

    range_start = 0
    range_end = 100
    default = 2

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
    Number of seconds for freeze, silence, and blind traps to take effect.
    """

    display_name = "Trap Duration"

    range_start = 1
    range_end = 60
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
    Disabling could lead to fill errors.
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
    Disabling could lead to fill errors.
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
    Disabling could lead to fill errors.
    """

    display_name = "Levelsanity"

    default = True

@dataclass
class WynncraftOptions(PerGameCommonOptions):
    goal_level: GoalLevel
    locked_region_enforcement: LockedRegionEnforcement
    locked_region_countdown: LockedRegionCountdown
    level_increment: LevelIncrement
    extra_max_levels: ExtraMaxLevels
    quest_checks: QuestChecks
    mini_quest_checks: MiniQuestChecks
    cave_checks: CaveChecks
    dungeon_checks: DungeonChecks
    level_checks: LevelChecks
    trap_chance: TrapChance
    freeze_trap_weight: FreezeTrapWeight
    silence_trap_weight: SilenceTrapWeight
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
        [LevelIncrement, ExtraMaxLevels]
    ),
    OptionGroup(
        "Location Options",
        [QuestChecks, MiniQuestChecks, CaveChecks, DungeonChecks, LevelChecks]
    ),
    OptionGroup(
        "Trap Options",
        [TrapChance, FreezeTrapWeight, SilenceTrapWeight, BlindTrapWeight, KillTrapWeight, TrapDuration]
    )
]

option_presets = {}
