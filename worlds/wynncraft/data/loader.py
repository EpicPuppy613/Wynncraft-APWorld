import csv
import os
from pkgutil import get_data

data = get_data(__name__, 'wynncraft-data.csv')
reader = csv.DictReader(data.decode("utf-8").splitlines())
rows = []

# csv column consts
NAME = "Content"
LEVEL = "Level"
TYPE = "Type"
AP = "AP"
ID = "ID (Hex)"
REGION = "Region/Connections"
CONNECTIONS = REGION

# run some preprocessing for future use
unlockable_regions = []
for row in reader:
    rows.append(row)
    if row[TYPE] == "Territory" and row["AP"] == "Item":
        unlockable_regions.append(row[NAME])