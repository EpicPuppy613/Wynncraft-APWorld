import csv
from pkgutil import get_data

data = get_data(__name__, "wynncraft-data.csv")
reader = csv.DictReader(data.decode("utf-8").splitlines())
rows = []

level_data = get_data(__name__, "wynncraft-levels.csv")
level_reader = csv.DictReader(level_data.decode("utf-8").splitlines())
level_rows = []

# csv column consts
NAME = "Content"
READY = "Ready"
LEVEL = "Level"
TYPE = "Type"
AP = "AP"
ID = "ID (Hex)"
REGION = "Region/Connections"
CONNECTIONS = REGION
PREREQS = "Prerequisites"
IS_PREREQ = "Is Prereq"
GEAR_REQ = "Gear Req"
ALT_LEVEL = "Alt Lvl."

LVL_REGIONS = "Regions"

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
    rows.append(row)

for level_row in level_reader:
    level_rows.append(level_row)
