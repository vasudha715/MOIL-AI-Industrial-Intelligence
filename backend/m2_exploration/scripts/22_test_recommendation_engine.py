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


# ==========================================
# IMPORT PANDAS
# ==========================================

import pandas as pd


# ==========================================
# IMPORT ENGINES
# ==========================================

from engine.prospectivity_engine import (

    calculate_prospectivity

)


from engine.recommendation_engine import (

    add_recommendations

)


# ==========================================
# INPUT FILE
# ==========================================

INPUT_FILE = (

    BASE_DIR

    / "data"

    / "processed"

    / "prospectivity_features.csv"

)


# ==========================================
# LOAD DATA
# ==========================================

print(

    "\n======================================"

)

print(

    "TESTING RECOMMENDATION ENGINE"

)

print(

    "======================================"

)


print(

    "\nLOADING DATA..."

)


df = pd.read_csv(

    INPUT_FILE

)


print(

    "TOTAL ZONES:",

    len(df)

)


# ==========================================
# CALCULATE PROSPECTIVITY
# ==========================================

print(

    "\nCALCULATING PROSPECTIVITY..."

)


df = calculate_prospectivity(

    df

)


# ==========================================
# ADD RECOMMENDATIONS
# ==========================================

print(

    "\nGENERATING RECOMMENDATIONS..."

)


df = add_recommendations(

    df

)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print(

    "\nFIRST 10 RESULTS:\n"

)


print(

    df[

        [

            "zone_id",

            "PROSPECTIVITY_SCORE",

            "PRIORITY",

            "EVIDENCE_CONFIDENCE",

            "EXPLANATION",

            "RECOMMENDATION"

        ]

    ]

    .head(10)

    .to_string(

        index=False

    )

)


# ==========================================
# PRIORITY SUMMARY
# ==========================================

print(

    "\nPRIORITY SUMMARY:\n"

)


print(

    df[

        "PRIORITY"

    ]

    .value_counts()

)


print(

    "\n======================================"

)

print(

    "RECOMMENDATION ENGINE WORKING"

)

print(

    "======================================"

)