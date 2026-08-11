import csv
import os
from pkgutil import get_data

data = get_data(__name__, "wynncraft-data.csv")
reader = csv.DictReader(data.decode("utf-8").splitlines())
rows = []

level_data = get_data(__name__, "wynncraft-levels.csv")
level_reader = csv.DictReader(level_data.decode("utf-8").splitlines())
level_rows = []
level_map = {}

# csv column consts
NAME = "Content"
READY = "Ready"
LEVEL = "Level"
TYPE = "Type"
AP = "AP"
ID = "ID (Hex)"
REGION = "Region/Connections"
CONNECTIONS = REGION
PREREQUISITES = "Prerequisites"
GEAR_REQ = "Gear Req"

# run some preprocessing for future use
for row in reader:
    if row[READY] != "TRUE":
        continue
    rows.append(row)

for level_row in level_reader:
    level_rows.append(level_row)
    level_map[level_row[LEVEL]] = level_row[REGION]
