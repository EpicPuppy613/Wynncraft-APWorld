import csv
import os
from pkgutil import get_data

data = get_data(__name__, 'wynncraft-data.csv')
reader = csv.DictReader(data.decode("utf-8").splitlines())
rows = []

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
all_regions = []
region_connections = {}
unlockable_regions = []
for row in reader:
    if row[TYPE] == "Region":
        all_regions.append(row[NAME])
        region_connections[row[NAME]] = row[CONNECTIONS]
    if row[READY] != "TRUE":
        continue
    rows.append(row)
    if row[TYPE] == "Region" and row["AP"] == "Item":
        unlockable_regions.append(row[NAME])