from services.aoi_service import search_location

from services.weather_service import get_weather
from services.weather_risk import calculate_weather_risk

from services.satellite_service import (
    search_sentinel2,
    select_best_image
)

from services.band_service import get_band_assets

from services.raster_service import read_band_aoi

from services.spectral_service import (
    calculate_spectral_features
)

from services.grid_service import (
    create_grid_features
)

from services.terrain_service import (
    get_elevations
)

from services.terrain_analysis_service import (
    calculate_terrain_features
)

from services.occurrence_service import (
    get_mineral_occurrences
)


import numpy as np
import pandas as pd


# ==========================================
# DISTANCE CALCULATION
# ==========================================

def calculate_distance_km(
    latitude1,
    longitude1,
    latitude2,
    longitude2
):

    earth_radius = 6371.0


    lat1 = np.radians(
        latitude1
    )

    lon1 = np.radians(
        longitude1
    )

    lat2 = np.radians(
        latitude2
    )

    lon2 = np.radians(
        longitude2
    )


    latitude_difference = (
        lat2 - lat1
    )

    longitude_difference = (
        lon2 - lon1
    )


    a = (

        np.sin(
            latitude_difference / 2
        ) ** 2

        +

        np.cos(lat1)

        *

        np.cos(lat2)

        *

        np.sin(
            longitude_difference / 2
        ) ** 2

    )


    c = (

        2

        *

        np.arctan2(

            np.sqrt(a),

            np.sqrt(1 - a)

        )

    )


    distance = (
        earth_radius * c
    )


    return distance


# ==========================================
# NORMALIZATION
# ==========================================

def normalize_series(series):

    minimum = (
        series.min()
    )

    maximum = (
        series.max()
    )


    if maximum == minimum:

        return pd.Series(

            np.ones(
                len(series)
            ),

            index=series.index

        )


    return (

        series - minimum

    ) / (

        maximum - minimum

    )


# ==========================================
# EXTRACT MANGANESE OCCURRENCES
# FROM USGS GEOJSON
# ==========================================

def extract_manganese_occurrences(
    geojson_data
):

    manganese_records = []


    if geojson_data is None:

        return manganese_records


    features = geojson_data.get(
        "features",
        []
    )


    for feature in features:

        properties = feature.get(
            "properties",
            {}
        )


        geometry = feature.get(
            "geometry",
            {}
        )


        # ----------------------------------
        # CHECK ALL POSSIBLE COMMODITY FIELDS
        # ----------------------------------

        commodity_values = []


        possible_fields = [

            "commod1",
            "commod2",
            "commod3",
            "commodity",
            "commodities"

        ]


        for field in possible_fields:

            value = str(

                properties.get(
                    field,
                    ""
                )

            ).upper()


            commodity_values.append(
                value
            )


        # ----------------------------------
        # COMBINE ALL COMMODITY INFORMATION
        # ----------------------------------

        combined_commodity = " ".join(
            commodity_values
        )


        # ----------------------------------
        # CHECK FOR MANGANESE
        # ----------------------------------

        if (

            "MANGANESE"
            not in combined_commodity

            and

            " MN "
            not in (
                " "
                + combined_commodity
                + " "
            )

        ):

            continue


        # ----------------------------------
        # GET COORDINATES
        # ----------------------------------

        coordinates = geometry.get(
            "coordinates"
        )


        if (

            coordinates is None

            or

            len(coordinates) < 2

        ):

            continue


        longitude = coordinates[0]

        latitude = coordinates[1]


        # ----------------------------------
        # GET SITE NAME
        # ----------------------------------

        site_name = (

            properties.get("dep_name")

            or

            properties.get("site_name")

            or

            properties.get("name")

            or

            "Unknown Site"

        )


        # ----------------------------------
        # SAVE MANGANESE RECORD
        # ----------------------------------

        manganese_records.append(

            {

                "site_name":
                    site_name,

                "commodity":
                    combined_commodity,

                "latitude":
                    latitude,

                "longitude":
                    longitude

            }

        )


    return manganese_records


# ==========================================
# MAIN EXPLORATION ENGINE
# ==========================================

def analyze_area(

    location_name,

    buffer_degrees=0.01,

    grid_rows=10,

    grid_cols=10

):


    print("\n======================================")
    print("MOIL AI COMPLETE EXPLORATION ENGINE")
    print("======================================")


    # ==================================
    # STEP 1 — LOCATION
    # ==================================

    print(
        "\nSTEP 1: SEARCHING LOCATION..."
    )


    location = search_location(
        location_name
    )


    if location is None:

        raise ValueError(
            "Location could not be found."
        )


    latitude = location[
        "latitude"
    ]


    longitude = location[
        "longitude"
    ]


    print(
        "LOCATION FOUND:"
    )

    print(
        location["name"]
    )


    print(
        "LATITUDE:",
        latitude
    )

    print(
        "LONGITUDE:",
        longitude
    )


    # ==================================
    # STEP 2 — WEATHER
    # ==================================

    print(
        "\nSTEP 2: GETTING WEATHER..."
    )


    weather = get_weather(

        latitude,

        longitude

    )


    weather_risk = (
        calculate_weather_risk(
            weather
        )
    )


    print(
        "WEATHER RISK:",
        weather_risk
    )


    # ==================================
    # STEP 3 — SATELLITE SEARCH
    # ==================================

    print(
        "\nSTEP 3: SEARCHING "
        "SENTINEL-2 SATELLITE..."
    )


    items = search_sentinel2(

        longitude=longitude,

        latitude=latitude,

        buffer_degrees=buffer_degrees

    )


    print(

        "SATELLITE IMAGES FOUND:",

        len(items)

    )


    if not items:

        raise ValueError(

            "No suitable Sentinel-2 "
            "satellite images found."

        )


    # ==================================
    # STEP 4 — BEST IMAGE
    # ==================================

    print(
        "\nSTEP 4: SELECTING "
        "BEST SATELLITE IMAGE..."
    )


    best_image = (
        select_best_image(
            items
        )
    )


    cloud_cover = (
        best_image.properties.get(
            "eo:cloud_cover"
        )
    )


    print(
        "BEST IMAGE:",
        best_image.id
    )


    print(
        "CLOUD COVER:",
        cloud_cover
    )


    # ==================================
    # STEP 5 — BAND ACCESS
    # ==================================

    print(
        "\nSTEP 5: ACCESSING "
        "SATELLITE BANDS..."
    )


    band_assets = (
        get_band_assets(
            best_image
        )
    )


    required_bands = [

        "B02",
        "B03",
        "B04",
        "B08",
        "B11",
        "B12"

    ]


    for band in required_bands:


        if band not in band_assets:

            raise ValueError(

                f"Required band {band} "
                "is not available."

            )


    print(
        "BANDS AVAILABLE:",
        list(
            band_assets.keys()
        )
    )


    # ==================================
    # STEP 6 — READ SATELLITE DATA
    # ==================================

    print(
        "\nSTEP 6: READING "
        "SATELLITE DATA..."
    )


    bands = {}


    for (
        band_name,
        band_url
    ) in band_assets.items():


        data, metadata = (
            read_band_aoi(

                band_url,

                longitude,

                latitude,

                buffer_degrees

            )
        )


        bands[
            band_name
        ] = data


        print(
            band_name,
            "SHAPE:",
            data.shape
        )


    # ==================================
    # STEP 7 — SPECTRAL FEATURES
    # ==================================

    print(
        "\nSTEP 7: CALCULATING "
        "SPECTRAL FEATURES..."
    )


    spectral_features = (

        calculate_spectral_features(
            bands
        )

    )


    print(
        "FEATURES:",
        list(
            spectral_features.keys()
        )
    )


    # ==================================
    # STEP 8 — EXPLORATION GRID
    # ==================================

    print(
        "\nSTEP 8: CREATING "
        "EXPLORATION GRID..."
    )


    exploration_grid = (

        create_grid_features(

            features=spectral_features,

            latitude=latitude,

            longitude=longitude,

            grid_rows=grid_rows,

            grid_cols=grid_cols,

            buffer_degrees=buffer_degrees

        )

    )


    print(
        "TOTAL EXPLORATION ZONES:",
        len(exploration_grid)
    )


    # ==================================
    # STEP 9 — ELEVATION
    # ==================================

    print(
        "\nSTEP 9: GETTING "
        "REAL ELEVATION DATA..."
    )


    latitudes = (

        exploration_grid[
            "center_lat"
        ].tolist()

    )


    longitudes = (

        exploration_grid[
            "center_lon"
        ].tolist()

    )


    elevations = (

        get_elevations(

            latitudes,

            longitudes

        )

    )


    exploration_grid[
        "ELEVATION_M"
    ] = elevations


    print(
        "ELEVATION DATA ADDED."
    )


    # ==================================
    # STEP 10 — TERRAIN ANALYSIS
    # ==================================

    print(
        "\nSTEP 10: CALCULATING "
        "TERRAIN FEATURES..."
    )


    exploration_grid = (

        calculate_terrain_features(
            exploration_grid,
            grid_rows=grid_rows,
            grid_cols=grid_cols
        )

    )


    print(
        "TERRAIN FEATURES ADDED."
    )


  

    # ==================================
    # STEP 13 — MANGANESE PROXIMITY
    # ==================================

    print(
        "\nSTEP 13: CALCULATING "
        "MANGANESE PROXIMITY..."
    )

    from services.proximity_service import (
        add_manganese_proximity
    )

    exploration_grid = add_manganese_proximity(
        exploration_grid
    )

    print(
        "MANGANESE PROXIMITY ADDED."
    )


    # ==================================
    # STEP 14 — SPECTRAL SCORE
    # ==================================

    print(
        "\nSTEP 14: CALCULATING "
        "PROSPECTIVITY SCORES..."
    )


    spectral_columns = [

        "NDVI",

        "NDMI",

        "RED_BLUE_RATIO",

        "SWIR_RATIO",

        "SWIR_NIR_RATIO",

        "NIR_RED_RATIO"

    ]


    normalized_features = []


    for column in spectral_columns:


        normalized_features.append(

            normalize_series(

                exploration_grid[
                    column
                ]

            )

        )


    exploration_grid[
        "SPECTRAL_SCORE"
    ] = (

        pd.concat(

            normalized_features,

            axis=1

        )

        .mean(axis=1)

    )


    # ==================================
    # TERRAIN SCORE
    # ==================================

    elevation_score = (

        normalize_series(

            exploration_grid[
                "ELEVATION_M"
            ]

        )

    )


    slope_score = (

        normalize_series(

            exploration_grid[
                "SLOPE_DEG"
            ]

        )

    )


    roughness_score = (

        normalize_series(

            exploration_grid[
                "TERRAIN_ROUGHNESS_M"
            ]

        )

    )


    exploration_grid[
        "TERRAIN_SCORE"
    ] = (

        elevation_score

        +

        slope_score

        +

        roughness_score

    ) / 3


    # ==================================
    # MANGANESE PROXIMITY SCORE
    # ==================================

    distance_series = (

        exploration_grid[
            "DISTANCE_TO_MN_KM"
        ]

    )


    if distance_series.notna().any():


        maximum_distance = (
            distance_series.max()
        )


        minimum_distance = (
            distance_series.min()
        )


        if (
            maximum_distance
            ==
            minimum_distance
        ):


            exploration_grid[
                "MN_PROXIMITY_SCORE"
            ] = 0.5


        else:


            exploration_grid[
                "MN_PROXIMITY_SCORE"
            ] = (

                maximum_distance

                -

                distance_series

            ) / (

                maximum_distance

                -

                minimum_distance

            )


    else:


        exploration_grid[
            "MN_PROXIMITY_SCORE"
        ] = 0.0


    # ==================================
    # FINAL PROSPECTIVITY SCORE
    # ==================================

    exploration_grid[
        "PROSPECTIVITY_SCORE"
    ] = (

        100

        *

        (

            0.40

            *

            exploration_grid[
                "SPECTRAL_SCORE"
            ]

            +

            0.30

            *

            exploration_grid[
                "TERRAIN_SCORE"
            ]

            +

            0.30

            *

            exploration_grid[
                "MN_PROXIMITY_SCORE"
            ]

        )

    )


    exploration_grid[
        "PROSPECTIVITY_SCORE"
    ] = (

        exploration_grid[
            "PROSPECTIVITY_SCORE"
        ].round(2)

    )


    # ==================================
    # STEP 15 — PRIORITY
    # ==================================

    print(
        "\nSTEP 15: ASSIGNING "
        "EXPLORATION PRIORITIES..."
    )


    def assign_priority(score):


        if score >= 60:

            return "HIGH"


        elif score >= 40:

            return "MODERATE"


        else:

            return "LOW"


    exploration_grid[
        "PRIORITY"
    ] = (

        exploration_grid[
            "PROSPECTIVITY_SCORE"
        ]

        .apply(
            assign_priority
        )

    )


    # ==================================
    # STEP 16 — RECOMMENDATIONS
    # ==================================

    print(
        "\nSTEP 16: GENERATING "
        "EXPLORATION RECOMMENDATIONS..."
    )


    def generate_recommendation(
        priority
    ):


        if priority == "HIGH":

            return (

                "Prioritize detailed "
                "geological mapping, "
                "ground validation, and "
                "targeted sampling."

            )


        elif priority == "MODERATE":

            return (

                "Conduct preliminary "
                "field reconnaissance "
                "and geological validation "
                "before further investment."

            )


        else:

            return (

                "Maintain as a lower-priority "
                "area. Reassess when additional "
                "geological evidence becomes "
                "available."

            )


    exploration_grid[
        "RECOMMENDATION"
    ] = (

        exploration_grid[
            "PRIORITY"
        ]

        .apply(
            generate_recommendation
        )

    )


    # ==================================
    # SORT RESULTS
    # ==================================

    exploration_grid = (

        exploration_grid

        .sort_values(

            by=
                "PROSPECTIVITY_SCORE",

            ascending=
                False

        )

        .reset_index(
            drop=True
        )

    )


    # ==================================
    # PRIORITY SUMMARY
    # ==================================

    priority_summary = (

        exploration_grid[
            "PRIORITY"
        ]

        .value_counts()

        .to_dict()

    )


    # ==================================
    # FINAL RESULT
    # ==================================

    result = {


        "location": {

            "name":
                location["name"],

            "latitude":
                latitude,

            "longitude":
                longitude

        },


        "weather":
            weather,


        "weather_risk":
            weather_risk,


        "satellite": {


            "image_id":
                best_image.id,


            "cloud_cover":
                cloud_cover

        },


        "total_zones":
            len(
                exploration_grid
            ),


        "priority_summary":
            priority_summary,


        "exploration_grid":
            exploration_grid

    }


    print(
        "\n======================================"
    )

    print(
        "COMPLETE EXPLORATION ANALYSIS FINISHED"
    )

    print(
        "======================================"
    )


    return result