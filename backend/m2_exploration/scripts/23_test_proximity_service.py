import sys
from pathlib import Path


# ==========================================
# PROJECT BASE DIRECTORY
# ==========================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


sys.path.append(
    str(BASE_DIR)
)


import pandas as pd


from services.proximity_service import (
    add_manganese_proximity
)


# ==========================================
# INPUT FILES
# ==========================================

ZONES_FILE = (

    BASE_DIR

    / "data"

    / "processed"

    / "exploration_terrain_features.csv"

)


OCCURRENCES_FILE = (

    BASE_DIR

    / "data"

    / "processed"

    / "occurrences"

    / "manganese_occurrences.csv"

)


# ==========================================
# START
# ==========================================

print(
    "\n======================================"
)

print(
    "TESTING PROXIMITY SERVICE"
)

print(
    "======================================"
)


# ==========================================
# LOAD DATA
# ==========================================

print(
    "\nLOADING EXPLORATION ZONES..."
)


zones_df = pd.read_csv(
    ZONES_FILE
)


print(
    "TOTAL ZONES:",
    len(zones_df)
)


print(
    "\nLOADING MANGANESE OCCURRENCES..."
)


occurrences_df = pd.read_csv(
    OCCURRENCES_FILE
)


print(
    "TOTAL MN OCCURRENCES:",
    len(occurrences_df)
)


# ==========================================
# CALCULATE PROXIMITY
# ==========================================

print(
    "\nCALCULATING MANGANESE PROXIMITY..."
)


result_df = (
    add_manganese_proximity(

        zones_dataframe=zones_df,

        occurrences_dataframe=occurrences_df

    )
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print(
    "\nFIRST 10 RESULTS:\n"
)


print(

    result_df[

        [

            "zone_id",

            "center_lat",

            "center_lon",

            "NEAREST_MN_SITE",

            "DISTANCE_TO_MN_KM"

        ]

    ]

    .head(10)

    .to_string(

        index=False

    )

)


# ==========================================
# SUCCESS
# ==========================================

print(
    "\n======================================"
)

print(
    "PROXIMITY SERVICE WORKING"
)

print(
    "======================================"
)