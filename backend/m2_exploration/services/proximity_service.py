import math

import pandas as pd

from pathlib import Path


# ==========================================
# PROJECT BASE DIRECTORY
# ==========================================

BASE_DIR = Path(
    __file__
).resolve().parent.parent


# ==========================================
# OCCURRENCE DATA
# ==========================================

OCCURRENCES_FILE = (

    BASE_DIR

    / "data"

    / "processed"

    / "occurrences"

    / "manganese_occurrences.csv"

)


# ==========================================
# HAVERSINE DISTANCE
# ==========================================

def calculate_distance_km(

    lat1,
    lon1,
    lat2,
    lon2

):

    earth_radius_km = 6371.0


    lat1_rad = math.radians(
        lat1
    )

    lon1_rad = math.radians(
        lon1
    )

    lat2_rad = math.radians(
        lat2
    )

    lon2_rad = math.radians(
        lon2
    )


    latitude_difference = (

        lat2_rad

        -

        lat1_rad

    )


    longitude_difference = (

        lon2_rad

        -

        lon1_rad

    )


    a = (

        math.sin(

            latitude_difference / 2

        ) ** 2


        +


        math.cos(
            lat1_rad
        )


        *


        math.cos(
            lat2_rad
        )


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


    return (

        earth_radius_km * c

    )


# ==========================================
# LOAD MANGANESE OCCURRENCES
# ==========================================

def load_manganese_occurrences():

    if not OCCURRENCES_FILE.exists():

        raise FileNotFoundError(

            "Manganese occurrence file "
            "was not found."

        )


    dataframe = pd.read_csv(

        OCCURRENCES_FILE

    )


    if dataframe.empty:

        raise ValueError(

            "No manganese occurrences "
            "are available."

        )


    return dataframe


# ==========================================
# ADD MANGANESE PROXIMITY
# ==========================================

def add_manganese_proximity(
    dataframe
):

    df = dataframe.copy()


    occurrences_df = (

        load_manganese_occurrences()

    )


    nearest_sites = []

    nearest_distances = []


    # ======================================
    # PROCESS EACH EXPLORATION ZONE
    # ======================================

    for _, zone in df.iterrows():


        zone_latitude = (

            zone[
                "center_lat"
            ]

        )


        zone_longitude = (

            zone[
                "center_lon"
            ]

        )


        minimum_distance = float(
            "inf"
        )


        nearest_site_name = None


        # ==================================
        # CHECK ALL MN OCCURRENCES
        # ==================================

        for _, occurrence in (

            occurrences_df.iterrows()

        ):


            distance = (

                calculate_distance_km(

                    zone_latitude,

                    zone_longitude,

                    occurrence[
                        "latitude"
                    ],

                    occurrence[
                        "longitude"
                    ]

                )

            )


            if distance < minimum_distance:


                minimum_distance = distance


                nearest_site_name = (

                    occurrence[
                        "site_name"
                    ]

                )


        nearest_sites.append(

            nearest_site_name

        )


        nearest_distances.append(

            round(

                minimum_distance,

                3

            )

        )


    # ======================================
    # ADD RESULTS
    # ======================================

    df[

        "NEAREST_MN_SITE"

    ] = nearest_sites


    df[

        "DISTANCE_TO_MN_KM"

    ] = nearest_distances


    return df