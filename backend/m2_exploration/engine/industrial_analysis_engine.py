from engine.exploration_engine import analyze_area


def analyze_industrial_area(
    location_name,
    buffer_degrees=0.01,
    grid_rows=10,
    grid_cols=10
):
    """
    Run the complete MOIL AI industrial exploration pipeline.

    The exploration engine already performs:
    Location -> Weather -> Satellite -> Spectral Features ->
    Grid -> Elevation -> Terrain -> Manganese Proximity ->
    Prospectivity -> Priority -> Recommendations.
    """

    print("\n======================================")
    print("MOIL AI INDUSTRIAL ANALYSIS ENGINE")
    print("======================================")

    result = analyze_area(
        location_name=location_name,
        buffer_degrees=buffer_degrees,
        grid_rows=grid_rows,
        grid_cols=grid_cols
    )

    exploration_grid = result["exploration_grid"].copy()

    top_zones = (
        exploration_grid
        .sort_values(
            "PROSPECTIVITY_SCORE",
            ascending=False
        )
        .head(10)
    )

    result["top_zones"] = top_zones

    print("\n======================================")
    print("INDUSTRIAL ANALYSIS COMPLETE")
    print("======================================")

    return result
