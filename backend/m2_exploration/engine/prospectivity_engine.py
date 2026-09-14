import pandas as pd
from sklearn.preprocessing import MinMaxScaler


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


def calculate_prospectivity(
    dataframe
):

    df = dataframe.copy()


    # ==========================================
    # NORMALIZE SPECTRAL FEATURES
    # ==========================================

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


    # ==========================================
    # NORMALIZE TERRAIN FEATURES
    # ==========================================

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
    # MANGANESE PROXIMITY
    #
    # Smaller distance = stronger evidence
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

        df["RED_BLUE_NORM"] * 0.30

        +

        df["SWIR_NORM"] * 0.25

        +

        df["SWIR_NIR_NORM"] * 0.20

        +

        df["NIR_RED_NORM"] * 0.15

        +

        df["NDMI_NORM"] * 0.10

    )


    # ==========================================
    # TERRAIN EVIDENCE
    # ==========================================

    df["TERRAIN_SCORE"] = (

        df["ELEVATION_NORM"] * 0.30

        +

        df["SLOPE_NORM"] * 0.40

        +

        df["ROUGHNESS_NORM"] * 0.30

    )


    # ==========================================
    # FINAL PROSPECTIVITY SCORE
    #
    # Satellite evidence  = 45%
    # Terrain evidence    = 20%
    # Mn occurrence       = 35%
    #
    # NOTE:
    # This is an evidence-based
    # prioritization score.
    # It is NOT a reserve estimate.
    # ==========================================

    df["PROSPECTIVITY_SCORE"] = (

        df["SPECTRAL_SCORE"] * 0.45

        +

        df["TERRAIN_SCORE"] * 0.20

        +

        df["MN_PROXIMITY_SCORE"] * 0.35

    ) * 100


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


    return df