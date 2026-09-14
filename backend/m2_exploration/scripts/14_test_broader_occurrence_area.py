import sys
from pathlib import Path


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
# BROADER ODISHA AREA
# ==========================================

MIN_LAT = 20.0
MIN_LON = 84.0

MAX_LAT = 23.0
MAX_LON = 87.0


# ==========================================
# DISPLAY
# ==========================================

print("\nTESTING BROADER MINERAL OCCURRENCE AREA")

print("\nSEARCH AREA:")

print(f"Latitude: {MIN_LAT} to {MAX_LAT}")

print(f"Longitude: {MIN_LON} to {MAX_LON}")


# ==========================================
# GET DATA
# ==========================================

data = get_mineral_occurrences(

    MIN_LAT,
    MIN_LON,
    MAX_LAT,
    MAX_LON

)


# ==========================================
# CHECK RESPONSE
# ==========================================

if data is None:

    print("\nFAILED!")

    print("Could not retrieve occurrence data.")


else:

    features = data.get("features", [])


    print("\nTOTAL OCCURRENCES FOUND:")

    print(len(features))


    # ==========================================
    # SHOW FIRST 10 RECORDS
    # ==========================================

    print("\nFIRST 10 RECORDS:")


    for index, feature in enumerate(features[:10]):

        properties = feature.get(
            "properties",
            {}
        )

        geometry = feature.get(
            "geometry",
            {}
        )


        print("\n--------------------------------")

        print(f"RECORD {index + 1}")

        print("\nSITE NAME:")

        print(
            properties.get(
                "site_name",
                "Unknown"
            )
        )


        print("\nCOMMODITY CODE:")

        print(
            properties.get(
                "code_list",
                "Unknown"
            )
        )


        print("\nDEVELOPMENT STATUS:")

        print(
            properties.get(
                "dev_stat",
                "Unknown"
            )
        )


        print("\nLOCATION:")

        print(geometry)


    print("\nSUCCESS!")

    print(
        "Broader occurrence search completed."
    )