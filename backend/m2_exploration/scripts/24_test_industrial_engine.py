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
# IMPORT ENGINE
# ==========================================

from engine.industrial_analysis_engine import (

    analyze_industrial_area

)


# ==========================================
# TEST
# ==========================================

print(

    "\n======================================"

)

print(

    "TESTING COMPLETE INDUSTRIAL ENGINE"

)

print(

    "======================================"

)


result = (

    analyze_industrial_area(

        location_name="Keonjhar, Odisha",

        buffer_degrees=0.01,

        grid_rows=10,

        grid_cols=10

    )

)


# ==========================================
# FINAL SUMMARY
# ==========================================

print(

    "\n======================================"

)

print(

    "FINAL INDUSTRIAL ANALYSIS SUMMARY"

)

print(

    "======================================"

)


print(

    "\nLOCATION:"

)

print(

    result["location"]

)


print(

    "\nSATELLITE:"

)

print(

    result["satellite"]

)


print(

    "\nWEATHER RISK:"

)

print(

    result["weather_risk"]

)


print(

    "\nTOTAL ZONES:"

)

print(

    result["total_zones"]

)


print(

    "\nPRIORITY SUMMARY:"

)

print(

    result["priority_summary"]

)


print(

    "\nTOP 10 EXPLORATION ZONES:"

)


print(

    result[

        "top_zones"

    ][

        [

            "zone_id",

            "center_lat",

            "center_lon",

            "PROSPECTIVITY_SCORE",

            "PRIORITY",

            "NEAREST_MN_SITE",

            "DISTANCE_TO_MN_KM"

        ]

    ]

    .to_string(

        index=False

    )

)


print(

    "\n======================================"

)

print(

    "COMPLETE INDUSTRIAL ENGINE WORKING"

)

print(

    "======================================"
)