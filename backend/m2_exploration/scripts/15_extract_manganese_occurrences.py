import sys
from pathlib import Path

import pandas as pd


# ==========================================
# PROJECT BASE DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))


# ==========================================
# IMPORT OCCURRENCE SERVICE
# ==========================================

from services.occurrence_service import (
    get_mineral_occurrences
)


# ==========================================
# SEARCH AREA
# ==========================================
#
# Broader Odisha region
#
# We use a larger area because a small
# selected area may not contain a recorded
# occurrence point.
# ==========================================

MIN_LAT = 20.0
MIN_LON = 84.0

MAX_LAT = 23.0
MAX_LON = 87.0


# ==========================================
# OUTPUT DIRECTORY
# ==========================================

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "occurrences"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


OUTPUT_FILE = (
    OUTPUT_DIR
    / "manganese_occurrences.csv"
)


# ==========================================
# START
# ==========================================

print("\nEXTRACTING MANGANESE OCCURRENCES")

print("\nSEARCH AREA:")

print(
    f"Latitude: "
    f"{MIN_LAT} to {MAX_LAT}"
)

print(
    f"Longitude: "
    f"{MIN_LON} to {MAX_LON}"
)


# ==========================================
# GET MINERAL OCCURRENCES
# ==========================================

data = get_mineral_occurrences(

    MIN_LAT,
    MIN_LON,
    MAX_LAT,
    MAX_LON

)


if data is None:

    print("\nERROR!")

    print(
        "Could not retrieve occurrence data."
    )

    sys.exit()


# ==========================================
# GET FEATURES
# ==========================================

features = data.get(
    "features",
    []
)


print("\nTOTAL MINERAL RECORDS:")

print(
    len(features)
)


# ==========================================
# STORE MANGANESE RECORDS
# ==========================================

manganese_records = []


# ==========================================
# LOOP THROUGH RECORDS
# ==========================================

for feature in features:


    properties = feature.get(
        "properties",
        {}
    )


    geometry = feature.get(
        "geometry",
        {}
    )


    # --------------------------------------
    # GET COMMODITY CODE
    # --------------------------------------

    commodity = str(

        properties.get(
            "code_list",
            ""
        )

    ).upper()


    # --------------------------------------
    # KEEP ONLY MANGANESE
    # --------------------------------------

    if "MN" not in commodity.split():

        continue


    # --------------------------------------
    # GET COORDINATES
    # --------------------------------------

    coordinates = geometry.get(
        "coordinates",
        None
    )


    if not coordinates:

        continue


    longitude = coordinates[0]

    latitude = coordinates[1]


    # --------------------------------------
    # CREATE CLEAN RECORD
    # --------------------------------------

    record = {

        "site_name":

            properties.get(
                "site_name",
                "Unknown"
            ),


        "commodity":

            commodity,


        "development_status":

            properties.get(
                "dev_stat",
                "Unknown"
            ),


        "latitude":

            latitude,


        "longitude":

            longitude,


        "source":

            "USGS MRDS"

    }


    manganese_records.append(
        record
    )


# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(
    manganese_records
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print(
    "\nTOTAL MANGANESE OCCURRENCES:"
)

print(
    len(df)
)


if len(df) > 0:


    print(
        "\nMANGANESE RECORDS:"
    )


    print(
        df.to_string(
            index=False
        )
    )


    # ======================================
    # SAVE CSV
    # ======================================

    df.to_csv(

        OUTPUT_FILE,

        index=False

    )


    print(
        "\nSAVED:"
    )


    print(
        OUTPUT_FILE
    )


    print(
        "\nSUCCESS!"
    )


    print(
        "Manganese occurrence data extracted."
    )


else:


    print(
        "\nWARNING!"
    )


    print(
        "No manganese occurrences found."
    )