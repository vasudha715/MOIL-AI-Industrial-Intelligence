import sys
from pathlib import Path

import pandas as pd


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


sys.path.append(
    str(BASE_DIR)
)


from engine.prospectivity_engine import (
    calculate_prospectivity
)


INPUT_FILE = (

    BASE_DIR

    / "data"

    / "processed"

    / "prospectivity_features.csv"

)


print("\n======================================")

print(
    "TESTING PROSPECTIVITY ENGINE"
)

print("======================================")


print(
    "\nLOADING DATA..."
)


df = pd.read_csv(
    INPUT_FILE
)


print(
    f"TOTAL ZONES: {len(df)}"
)


print(
    "\nCALCULATING PROSPECTIVITY..."
)


result = calculate_prospectivity(
    df
)


print(
    "\nFIRST 10 RESULTS:\n"
)


print(

    result[

        [

            "zone_id",

            "SPECTRAL_SCORE",

            "TERRAIN_SCORE",

            "MN_PROXIMITY_SCORE",

            "PROSPECTIVITY_SCORE",

            "PRIORITY"

        ]

    ]

    .head(10)

    .to_string(
        index=False
    )

)


print(
    "\nPRIORITY SUMMARY:\n"
)


print(

    result[
        "PRIORITY"
    ]

    .value_counts()

)


print(
    "\n======================================"
)

print(
    "PROSPECTIVITY ENGINE WORKING"
)

print(
    "======================================"
)