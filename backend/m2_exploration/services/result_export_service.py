import json

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


# ==========================================
# OUTPUT DIRECTORY
# ==========================================

OUTPUT_DIR = (
    BASE_DIR
    / "outputs"
)


# ==========================================
# CREATE OUTPUT DIRECTORY
# ==========================================

OUTPUT_DIR.mkdir(
    exist_ok=True
)


# ==========================================
# EXPORT INDUSTRIAL RESULTS
# ==========================================

def export_industrial_results(result):

    print(
        "\n======================================"
    )

    print(
        "EXPORTING INDUSTRIAL ANALYSIS RESULTS"
    )

    print(
        "======================================"
    )


    # ======================================
    # GET DATA
    # ======================================

    exploration_grid = (
        result["exploration_grid"]
    )


    top_zones = (
        result["top_zones"]
    )


    # ======================================
    # FILE PATHS
    # ======================================

    exploration_file = (
        OUTPUT_DIR
        / "exploration_results.csv"
    )


    top_zones_file = (
        OUTPUT_DIR
        / "top_10_zones.csv"
    )


    summary_file = (
        OUTPUT_DIR
        / "analysis_summary.json"
    )


    # ======================================
    # SAVE EXPLORATION GRID
    # ======================================

    exploration_grid.to_csv(

        exploration_file,

        index=False

    )


    print(

        "EXPLORATION RESULTS SAVED:"

    )

    print(
        exploration_file
    )


    # ======================================
    # SAVE TOP ZONES
    # ======================================

    top_zones.to_csv(

        top_zones_file,

        index=False

    )


    print(

        "TOP 10 ZONES SAVED:"

    )

    print(
        top_zones_file
    )


    # ======================================
    # CREATE SUMMARY
    # ======================================

    summary = {

        "location":

            result["location"],


        "satellite":

            result["satellite"],


        "weather_risk":

            result["weather_risk"],


        "total_zones":

            result["total_zones"],


        "priority_summary":

            result["priority_summary"]

    }


    # ======================================
    # SAVE JSON SUMMARY
    # ======================================

    with open(

        summary_file,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            summary,

            file,

            indent=4

        )


    print(

        "ANALYSIS SUMMARY SAVED:"

    )

    print(
        summary_file
    )


    print(

        "\n======================================"

    )

    print(

        "RESULT EXPORT COMPLETED"

    )

    print(

        "======================================"

    )


    return {

        "exploration_results":

            str(
                exploration_file
            ),


        "top_zones":

            str(
                top_zones_file
            ),


        "summary":

            str(
                summary_file
            )

    }