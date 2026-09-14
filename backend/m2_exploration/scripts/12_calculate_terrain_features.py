import sys

from pathlib import Path

import pandas as pd


# ----------------------------------
# BASE DIRECTORY
# ----------------------------------

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


sys.path.append(
    str(BASE_DIR)
)


# ----------------------------------
# IMPORT TERRAIN ANALYSIS
# ----------------------------------

from services.terrain_analysis_service import (
    calculate_terrain_features
)


# ----------------------------------
# INPUT FILE
# ----------------------------------

input_path = (

    BASE_DIR
    / "data"
    / "processed"
    / "exploration_terrain.csv"

)


# ----------------------------------
# OUTPUT FILE
# ----------------------------------

output_path = (

    BASE_DIR
    / "data"
    / "processed"
    / "exploration_terrain_features.csv"

)


# ----------------------------------
# LOAD DATA
# ----------------------------------

print(
    "\nLOADING TERRAIN DATA..."
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
# CALCULATE TERRAIN FEATURES
# ----------------------------------

print(
    "\nCALCULATING TERRAIN FEATURES..."
)


df = calculate_terrain_features(

    df,

    grid_rows=10,

    grid_cols=10

)


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

            "ELEVATION_M",

            "SLOPE_DEG",

            "TERRAIN_ROUGHNESS_M"

        ]

    ].head(10)

)


# ----------------------------------
# SAVE
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
    "Terrain features calculated "
    "successfully."
)