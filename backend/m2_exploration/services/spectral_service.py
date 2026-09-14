import numpy as np


def resample_to_shape(data, target_shape):
    """
    Resample lower-resolution data to match
    the target shape.
    """

    source_height, source_width = data.shape
    target_height, target_width = target_shape

    row_indices = np.linspace(
        0,
        source_height - 1,
        target_height
    ).astype(int)

    column_indices = np.linspace(
        0,
        source_width - 1,
        target_width
    ).astype(int)

    return data[
        np.ix_(
            row_indices,
            column_indices
        )
    ]


def safe_divide(numerator, denominator):
    """
    Safely divide two arrays and convert
    invalid values to NaN.
    """

    numerator = numerator.astype(np.float32)
    denominator = denominator.astype(np.float32)

    with np.errstate(
        divide="ignore",
        invalid="ignore"
    ):

        result = np.divide(
            numerator,
            denominator
        )

        result[
            ~np.isfinite(result)
        ] = np.nan

    return result


def calculate_spectral_features(bands):
    """
    Calculate satellite-derived spectral
    features from Sentinel-2 bands.
    """

    # ----------------------------------
    # 10 METRE BANDS
    # ----------------------------------

    b02 = bands["B02"].astype(np.float32)
    b03 = bands["B03"].astype(np.float32)
    b04 = bands["B04"].astype(np.float32)
    b08 = bands["B08"].astype(np.float32)


    # ----------------------------------
    # TARGET SHAPE
    # ----------------------------------

    target_shape = b04.shape


    # ----------------------------------
    # RESAMPLE 20 METRE BANDS
    # ----------------------------------

    b11 = resample_to_shape(
        bands["B11"],
        target_shape
    ).astype(np.float32)


    b12 = resample_to_shape(
        bands["B12"],
        target_shape
    ).astype(np.float32)


    # ----------------------------------
    # FEATURE 1 — NDVI
    # Vegetation indicator
    # ----------------------------------

    ndvi = safe_divide(

        b08 - b04,

        b08 + b04

    )


    # ----------------------------------
    # FEATURE 2 — NDMI
    # Moisture indicator
    # ----------------------------------

    ndmi = safe_divide(

        b08 - b11,

        b08 + b11

    )


    # ----------------------------------
    # FEATURE 3 — RED / BLUE RATIO
    # General spectral indicator
    # ----------------------------------

    red_blue_ratio = safe_divide(

        b04,

        b02

    )


    # ----------------------------------
    # FEATURE 4 — SWIR1 / SWIR2
    # SWIR spectral contrast
    # ----------------------------------

    swir_ratio = safe_divide(

        b11,

        b12

    )


    # ----------------------------------
    # FEATURE 5 — SWIR1 / NIR
    # ----------------------------------

    swir_nir_ratio = safe_divide(

        b11,

        b08

    )


    # ----------------------------------
    # FEATURE 6 — NIR / RED
    # ----------------------------------

    nir_red_ratio = safe_divide(

        b08,

        b04

    )


    # ----------------------------------
    # RETURN FEATURES
    # ----------------------------------

    return {

        "NDVI": ndvi,

        "NDMI": ndmi,

        "RED_BLUE_RATIO": red_blue_ratio,

        "SWIR_RATIO": swir_ratio,

        "SWIR_NIR_RATIO": swir_nir_ratio,

        "NIR_RED_RATIO": nir_red_ratio

    }


def calculate_feature_statistics(data):
    """
    Calculate statistics for a feature.
    """

    valid_data = data[
        np.isfinite(data)
    ]


    if valid_data.size == 0:

        return {

            "min": None,

            "max": None,

            "mean": None,

            "median": None,

            "valid_pixels": 0

        }


    return {

        "min": float(
            np.min(valid_data)
        ),

        "max": float(
            np.max(valid_data)
        ),

        "mean": float(
            np.mean(valid_data)
        ),

        "median": float(
            np.median(valid_data)
        ),

        "valid_pixels": int(
            valid_data.size
        )

    }