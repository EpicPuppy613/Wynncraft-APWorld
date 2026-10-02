import csv
from pkgutil import get_data

data = get_data(__name__, "wynncraft-data.csv")
reader = csv.DictReader(data.decode("utf-8").splitlines())
rows = []
prereqs = {}

level_data = get_data(__name__, "wynncraft-levels.csv")
level_reader = csv.DictReader(level_data.decode("utf-8").splitlines())
level_rows = []

access_data = get_data(__name__, "wynncraft-access.csv")
access_reader = csv.DictReader(access_data.decode("utf-8").splitlines())
access_rows = []

# csv column consts
NAME = "Content"
READY = "Ready"
LEVEL = "Level"
TYPE = "Type"
AP = "AP"
ID = "ID (Hex)"
REGION = "Region/Connections"
ALT_REGIONS = "Alt Regions"
CONNECTIONS = REGION
PREREQS = "Prerequisites"
IS_PREREQ = "Is Prereq"
GEAR_REQ = "Gear Req"
ALT_LEVEL = "Alt Lvl."

LVL_REGIONS = "Regions"
ACCESS_REGION = "Region"

LIST_COLUMNS = [REGION, ALT_REGIONS, PREREQS, LVL_REGIONS]

def build_row(in_row: dict[str, str]) -> dict[str, str]:
    built_row = {}
    for entry in in_row:
        if entry in LIST_COLUMNS:
            split = in_row[entry].split(", ")
            if split[0] == "":
                built_row[entry] = []
            else:
                built_row[entry] = list(map(lambda e: e.replace(";", ","), split))
        else:
            built_row[entry] = in_row[entry].replace(";", ",")
    return built_row

# run some preprocessing for future use
all_dungeons = {}
all_quests = {}
for row in reader:
    if row[READY] != "TRUE":
        continue
    elif row[TYPE] == "Dungeon" or row[TYPE] == "C-Dungeon":
        all_dungeons[row[NAME].split(": ")[1]] = int(row[LEVEL])
    elif row[TYPE] == "Quest":
        all_quests[row[NAME].split(": ")[1]] = int(row[LEVEL])

    if row[IS_PREREQ] == "TRUE":
        prereqs[row[NAME]] = build_row(row)

    rows.append(build_row(row))

for level_row in level_reader:
    level_rows.append(build_row(level_row))

for access_row in access_reader:
    access_rows.append(build_row(access_row))