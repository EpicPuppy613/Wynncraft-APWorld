import csv
import os

file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wynncraft-data.csv'))
reader = csv.DictReader(file)
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