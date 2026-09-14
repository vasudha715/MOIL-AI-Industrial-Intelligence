import math
from pathlib import Path

import pandas as pd


# ==========================================
# PROJECT BASE DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


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
# OUTPUT FILE
# ==========================================

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "exploration_mn_proximity.csv"
)


# ==========================================
# HAVERSINE DISTANCE FUNCTION
# ==========================================

def calculate_distance_km(
    lat1,
    lon1,
    lat2,
    lon2
):
    """
    Calculate geographic distance between
    two latitude/longitude coordinates.

    Returns distance in kilometres.
    """

    earth_radius_km = 6371.0


    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)

    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)


    latitude_difference = (
        lat2_rad - lat1_rad
    )

    longitude_difference = (
        lon2_rad - lon1_rad
    )


    a = (

        math.sin(
            latitude_difference / 2
        ) ** 2

        +

        math.cos(lat1_rad)

        *

        math.cos(lat2_rad)

        *

        math.sin(
            longitude_difference / 2
        ) ** 2

    )


    c = (

        2

        *

        math.atan2(

            math.sqrt(a),

            math.sqrt(1 - a)

        )

    )


    distance = (

        earth_radius_km * c

    )


    return distance


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
    f"\nTOTAL ZONES: "
    f"{len(zones_df)}"
)


print(
    "\nLOADING MANGANESE OCCURRENCES..."
)


occurrences_df = pd.read_csv(
    OCCURRENCES_FILE
)


print(
    f"\nTOTAL MN OCCURRENCES: "
    f"{len(occurrences_df)}"
)


# ==========================================
# STORE RESULTS
# ==========================================

nearest_sites = []

nearest_distances = []


# ==========================================
# PROCESS EVERY ZONE
# ==========================================

print(
    "\nCALCULATING MANGANESE PROXIMITY..."
)


for _, zone in zones_df.iterrows():


    zone_latitude = (
        zone["center_lat"]
    )


    zone_longitude = (
        zone["center_lon"]
    )


    minimum_distance = float("inf")

    nearest_site_name = None


    # --------------------------------------
    # COMPARE WITH EVERY MN OCCURRENCE
    # --------------------------------------

    for _, occurrence in (
        occurrences_df.iterrows()
    ):


        occurrence_latitude = (
            occurrence["latitude"]
        )


        occurrence_longitude = (
            occurrence["longitude"]
        )


        distance = calculate_distance_km(

            zone_latitude,

            zone_longitude,

            occurrence_latitude,

            occurrence_longitude

        )


        # ----------------------------------
        # FIND NEAREST
        # ----------------------------------

        if distance < minimum_distance:


            minimum_distance = distance


            nearest_site_name = (

                occurrence[
                    "site_name"
                ]

            )


    # --------------------------------------
    # SAVE RESULT
    # --------------------------------------

    nearest_sites.append(
        nearest_site_name
    )


    nearest_distances.append(
        round(
            minimum_distance,
            3
        )
    )


# ==========================================
# ADD RESULTS TO DATASET
# ==========================================

zones_df[
    "NEAREST_MN_SITE"
] = nearest_sites


zones_df[
    "DISTANCE_TO_MN_KM"
] = nearest_distances


# ==========================================
# DISPLAY RESULTS
# ==========================================

print(
    "\nFIRST 10 ZONES:"
)


print(

    zones_df[

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
# SAVE OUTPUT
# ==========================================

zones_df.to_csv(

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
    "Manganese proximity added "
    "to all exploration zones."
)