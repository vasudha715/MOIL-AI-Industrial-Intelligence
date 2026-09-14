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
# IMPORT SERVICE
# ==========================================

from services.occurrence_service import (
    get_mineral_occurrences
)


# ==========================================
# TEST LOCATION
# ==========================================

# Keonjhar, Odisha

MIN_LAT = 21.45
MIN_LON = 85.45

MAX_LAT = 21.55
MAX_LON = 85.55


# ==========================================
# DISPLAY
# ==========================================

print(
    "\nTESTING MINERAL OCCURRENCE SERVICE"
)


print(
    "\nSEARCH AREA:"
)


print(
    f"Latitude: "
    f"{MIN_LAT} to {MAX_LAT}"
)


print(
    f"Longitude: "
    f"{MIN_LON} to {MAX_LON}"
)


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

    print(
        "\nFAILED!"
    )

    print(
        "Could not retrieve occurrence data."
    )


else:

    features = data.get(

        "features",

        []

    )


    print(
        "\nTOTAL OCCURRENCES FOUND:"
    )


    print(
        len(features)
    )


    # --------------------------------------
    # SHOW FIRST 5
    # --------------------------------------

    print(
        "\nFIRST 5 RECORDS:"
    )


    for index, feature in enumerate(
        features[:5]
    ):


        properties = feature.get(

            "properties",

            {}

        )


        geometry = feature.get(

            "geometry",

            {}

        )


        print(
            "\n--------------------"
        )


        print(
            f"RECORD {index + 1}"
        )


        print(
            "PROPERTIES:"
        )


        print(
            properties
        )


        print(
            "GEOMETRY:"
        )


        print(
            geometry
        )


    print(
        "\nSUCCESS!"
    )


    print(
        "Occurrence service is working."
    )