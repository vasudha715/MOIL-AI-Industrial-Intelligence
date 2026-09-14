from pathlib import Path

import pandas as pd

from sklearn.preprocessing import MinMaxScaler


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
    / "prospectivity_features.csv"
)


# ==========================================
# OUTPUT FILE
# ==========================================

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "prospectivity_scores.csv"
)


# ==========================================
# LOAD DATA
# ==========================================

print("\nCALCULATING PROSPECTIVITY SCORES")


print("\nLOADING DATA...")


df = pd.read_csv(
    INPUT_FILE
)


print(
    f"\nTOTAL ZONES: {len(df)}"
)


# ==========================================
# NORMALIZATION FUNCTION
# ==========================================

def normalize_column(
    dataframe,
    column_name
):

    scaler = MinMaxScaler()


    values = dataframe[
        [column_name]
    ]


    normalized_values = (
        scaler.fit_transform(values)
        .flatten()
    )


    return normalized_values


# ==========================================
# NORMALIZE FEATURES
# ==========================================

print(
    "\nNORMALIZING FEATURES..."
)


df["NDVI_NORM"] = normalize_column(
    df,
    "NDVI"
)


df["NDMI_NORM"] = normalize_column(
    df,
    "NDMI"
)


df["RED_BLUE_NORM"] = normalize_column(
    df,
    "RED_BLUE_RATIO"
)


df["SWIR_NORM"] = normalize_column(
    df,
    "SWIR_RATIO"
)


df["SWIR_NIR_NORM"] = normalize_column(
    df,
    "SWIR_NIR_RATIO"
)


df["NIR_RED_NORM"] = normalize_column(
    df,
    "NIR_RED_RATIO"
)


df["ELEVATION_NORM"] = normalize_column(
    df,
    "ELEVATION_M"
)


df["SLOPE_NORM"] = normalize_column(
    df,
    "SLOPE_DEG"
)


df["ROUGHNESS_NORM"] = normalize_column(
    df,
    "TERRAIN_ROUGHNESS_M"
)


# ==========================================
# MANGANESE PROXIMITY SCORE
#
# Smaller distance = higher evidence
# ==========================================

df["MN_PROXIMITY_SCORE"] = (

    1

    -

    normalize_column(

        df,

        "DISTANCE_TO_MN_KM"

    )

)


# ==========================================
# SPECTRAL EVIDENCE
# ==========================================

df["SPECTRAL_SCORE"] = (

    (
        df["RED_BLUE_NORM"] * 0.30
    )

    +

    (
        df["SWIR_NORM"] * 0.25
    )

    +

    (
        df["SWIR_NIR_NORM"] * 0.20
    )

    +

    (
        df["NIR_RED_NORM"] * 0.15
    )

    +

    (
        df["NDMI_NORM"] * 0.10
    )

)


# ==========================================
# TERRAIN EVIDENCE
# ==========================================

df["TERRAIN_SCORE"] = (

    (
        df["ELEVATION_NORM"] * 0.30
    )

    +

    (
        df["SLOPE_NORM"] * 0.40
    )

    +

    (
        df["ROUGHNESS_NORM"] * 0.30
    )

)


# ==========================================
# FINAL PROSPECTIVITY SCORE
#
# Spectral: 40%
# Terrain: 20%
# Mn proximity: 40%
# ==========================================

df["PROSPECTIVITY_SCORE"] = (

    (

        df["SPECTRAL_SCORE"]
        * 0.40

    )

    +

    (

        df["TERRAIN_SCORE"]
        * 0.20

    )

    +

    (

        df["MN_PROXIMITY_SCORE"]
        * 0.40

    )

) * 100


# ==========================================
# ROUND SCORE
# ==========================================

df["PROSPECTIVITY_SCORE"] = (

    df["PROSPECTIVITY_SCORE"]
    .round(2)

)


# ==========================================
# PRIORITY CLASSIFICATION
# ==========================================

def classify_priority(
    score
):

    if score < 40:

        return "LOW"


    elif score < 60:

        return "MODERATE"


    elif score < 80:

        return "HIGH"


    else:

        return "VERY HIGH"


df["PRIORITY"] = (

    df[
        "PROSPECTIVITY_SCORE"
    ]

    .apply(
        classify_priority
    )

)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print(
    "\nFIRST 10 RESULTS:"
)


print(

    df[

        [

            "zone_id",

            "SPECTRAL_SCORE",

            "TERRAIN_SCORE",

            "MN_PROXIMITY_SCORE",

            "PROSPECTIVITY_SCORE",

            "PRIORITY"

        ]

    ]

    .head(10)

    .to_string(

        index=False

    )

)


# ==========================================
# PRIORITY SUMMARY
# ==========================================

print(
    "\nPRIORITY SUMMARY:"
)


print(

    df[
        "PRIORITY"
    ]

    .value_counts()

)


# ==========================================
# SAVE RESULTS
# ==========================================

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
    "Prospectivity scores calculated."
)