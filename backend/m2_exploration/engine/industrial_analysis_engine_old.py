from engine.exploration_engine import (
    analyze_area
)

from engine.prospectivity_engine import (
    calculate_prospectivity
)

from engine.recommendation_engine import (
    add_recommendations
)

from services.terrain_service import (
    get_elevations
)

from services.terrain_analysis_service import (
    calculate_terrain_features
)


def analyze_industrial_area(
    location_name,
    buffer_degrees=0.01,
    grid_rows=10,
    grid_cols=10
):
    """
    Complete industrial exploration analysis.

    Pipeline:

    Location
        ↓
    Weather
        ↓
    Satellite
        ↓
    Spectral Features
        ↓
    Exploration Grid
        ↓
    Terrain Features
        ↓
    Manganese Proximity
        ↓
    Prospectivity
        ↓
    Recommendations
    """


    print(
        "\n======================================"
    )

    print(
        "MOIL AI INDUSTRIAL ANALYSIS ENGINE"
    )

    print(
        "======================================"
    )


    # ======================================
    # STEP 1
    # INITIAL EXPLORATION
    # ======================================

    exploration_result = analyze_area(

        location_name=location_name,

        buffer_degrees=buffer_degrees,

        grid_rows=grid_rows,

        grid_cols=grid_cols

    )


    exploration_grid = (
        exploration_result[
            "exploration_grid"
        ].copy()
    )


    print(
        "\nSTEP 9: GETTING TERRAIN ELEVATION..."
    )


    latitudes = (

        exploration_grid[
            "center_lat"
        ]
        .tolist()

    )


    longitudes = (

        exploration_grid[
            "center_lon"
        ]
        .tolist()

    )


    elevations = get_elevations(

        latitudes,

        longitudes

    )


    exploration_grid[
        "ELEVATION_M"
    ] = elevations


    print(
        "ELEVATION DATA ADDED."
    )


    # ======================================
    # STEP 10
    # TERRAIN FEATURES
    # ======================================

    print(
        "\nSTEP 10: CALCULATING TERRAIN FEATURES..."
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


    # ======================================
    # STEP 11
    # MANGANESE PROXIMITY
    # ======================================

    print(
        "\nSTEP 11: ADDING MANGANESE PROXIMITY..."
    )


    from services.proximity_service import (
        add_manganese_proximity
    )


    exploration_grid = (
        add_manganese_proximity(
            exploration_grid
        )
    )


    print(
        "MANGANESE PROXIMITY ADDED."
    )


    # ======================================
    # STEP 12
    # PROSPECTIVITY
    # ======================================

    print(
        "\nSTEP 12: CALCULATING PROSPECTIVITY..."
    )


    exploration_grid = (
        calculate_prospectivity(
            exploration_grid
        )
    )


    print(
        "PROSPECTIVITY SCORES ADDED."
    )


    # ======================================
    # STEP 13
    # RECOMMENDATIONS
    # ======================================

    print(
        "\nSTEP 13: GENERATING RECOMMENDATIONS..."
    )


    exploration_grid = (
        add_recommendations(
            exploration_grid
        )
    )


    print(
        "RECOMMENDATIONS ADDED."
    )


    # ======================================
    # PRIORITY SUMMARY
    # ======================================

    priority_summary = (

        exploration_grid[
            "PRIORITY"
        ]

        .value_counts()

        .to_dict()

    )


    # ======================================
    # TOP PRIORITY ZONES
    # ======================================

    top_zones = (

        exploration_grid

        .sort_values(

            "PROSPECTIVITY_SCORE",

            ascending=False

        )

        .head(10)

    )


    # ======================================
    # FINAL RESULT
    # ======================================

    result = {

        "location":

            exploration_result[
                "location"
            ],


        "weather":

            exploration_result[
                "weather"
            ],


        "weather_risk":

            exploration_result[
                "weather_risk"
            ],


        "satellite":

            exploration_result[
                "satellite"
            ],


        "priority_summary":

            priority_summary,


        "total_zones":

            len(
                exploration_grid
            ),


        "top_zones":

            top_zones,


        "exploration_grid":

            exploration_grid

    }


    print(
        "\n======================================"
    )

    print(
        "INDUSTRIAL ANALYSIS COMPLETE"
    )

    print(
        "======================================"
    )


    return result