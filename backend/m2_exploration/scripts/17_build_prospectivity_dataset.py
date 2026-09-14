from pathlib import Path

import pandas as pd


# ==========================================
# PROJECT BASE DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# INPUT FILE
# ==========================================

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "exploration_mn_proximity.csv"
)


# ==========================================
# OUTPUT DIRECTORY
# ==========================================

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# OUTPUT FILE
# ==========================================

OUTPUT_FILE = (
    OUTPUT_DIR
    / "prospectivity_features.csv"
)


# ==========================================
# START
# ==========================================

print(
    "\nBUILDING PROSPECTIVITY FEATURE DATASET"
)


# ==========================================
# LOAD DATA
# ==========================================

print(
    "\nLOADING DATA..."
)


df = pd.read_csv(
    INPUT_FILE
)


print(
    f"\nTOTAL ZONES: {len(df)}"
)


# ==========================================
# REQUIRED COLUMNS
# ==========================================

required_columns = [

    # Zone information

    "zone_id",

    "grid_row",

    "grid_col",

    "center_lat",

    "center_lon",


    # Satellite features

    "NDVI",

    "NDMI",

    "RED_BLUE_RATIO",

    "SWIR_RATIO",

    "SWIR_NIR_RATIO",

    "NIR_RED_RATIO",


    # Terrain features

    "ELEVATION_M",

    "SLOPE_DEG",

    "TERRAIN_ROUGHNESS_M",


    # Mineral occurrence evidence

    "NEAREST_MN_SITE",

    "DISTANCE_TO_MN_KM"

]


# ==========================================
# CHECK COLUMNS
# ==========================================

print(
    "\nCHECKING REQUIRED FEATURES..."
)


missing_columns = [

    column

    for column in required_columns

    if column not in df.columns

]


if missing_columns:

    print(
        "\nERROR!"
    )

    print(
        "MISSING COLUMNS:"
    )

    print(
        missing_columns
    )

    raise ValueError(
        "Required features are missing."
    )


print(
    "\nALL REQUIRED FEATURES FOUND!"
)


# ==========================================
# SELECT FEATURES
# ==========================================

prospectivity_df = df[
    required_columns
].copy()


# ==========================================
# CHECK MISSING VALUES
# ==========================================

print(
    "\nCHECKING MISSING VALUES..."
)


missing_values = (
    prospectivity_df
    .isnull()
    .sum()
)


print(
    missing_values
)


# ==========================================
# DISPLAY FIRST RECORDS
# ==========================================

print(
    "\nFIRST 5 RECORDS:"
)


print(

    prospectivity_df

    .head()

    .to_string(
        index=False
    )

)


# ==========================================
# SAVE DATASET
# ==========================================

prospectivity_df.to_csv(

    OUTPUT_FILE,

    index=False

)


print(
    "\nSAVED:"
)


print(
    OUTPUT_FILE
)


# ==========================================
# SUCCESS
# ==========================================

print(
    "\nSUCCESS!"
)


print(
    "Prospectivity feature dataset created."
)