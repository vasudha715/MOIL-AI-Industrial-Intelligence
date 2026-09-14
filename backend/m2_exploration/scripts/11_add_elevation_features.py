import sys

from pathlib import Path

import pandas as pd


# ----------------------------------
# PROJECT BASE DIRECTORY
# ----------------------------------

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


# ----------------------------------
# ALLOW IMPORTS FROM PROJECT
# ----------------------------------

sys.path.append(
    str(BASE_DIR)
)


# ----------------------------------
# IMPORT TERRAIN SERVICE
# ----------------------------------

from services.terrain_service import (
    get_elevations
)


# ----------------------------------
# INPUT FILE
# ----------------------------------

input_path = (

    BASE_DIR
    / "data"
    / "processed"
    / "exploration_grid.csv"

)


# ----------------------------------
# OUTPUT FILE
# ----------------------------------

output_path = (

    BASE_DIR
    / "data"
    / "processed"
    / "exploration_terrain.csv"

)


# ----------------------------------
# LOAD EXPLORATION DATA
# ----------------------------------

print(
    "\nLOADING EXPLORATION GRID..."
)


df = pd.read_csv(
    input_path
)


print(
    "\nTOTAL ZONES:"
)

print(
    len(df)
)


# ----------------------------------
# EXTRACT COORDINATES
# ----------------------------------

latitudes = df[
    "center_lat"
].tolist()


longitudes = df[
    "center_lon"
].tolist()


# ----------------------------------
# GET REAL ELEVATIONS
# ----------------------------------

print(
    "\nGETTING REAL ELEVATION DATA..."
)


elevations = get_elevations(

    latitudes,

    longitudes

)


# ----------------------------------
# ADD ELEVATION
# ----------------------------------

df[
    "ELEVATION_M"
] = elevations


# ----------------------------------
# DISPLAY RESULTS
# ----------------------------------

print(
    "\nFIRST 10 ZONES:"
)


print(

    df[

        [

            "zone_id",

            "center_lat",

            "center_lon",

            "ELEVATION_M"

        ]

    ].head(10)

)


# ----------------------------------
# SAVE FILE
# ----------------------------------

df.to_csv(

    output_path,

    index=False

)


print(
    "\nSAVED:"
)

print(
    output_path
)


# ----------------------------------
# SUCCESS
# ----------------------------------

print(
    "\nSUCCESS!"
)

print(
    "Elevation features added "
    "to all exploration zones."
)