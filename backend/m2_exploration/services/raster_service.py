import rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
import numpy as np


def read_band_aoi(
    band_url,
    longitude,
    latitude,
    buffer_degrees=0.01
):
    """
    Reads a small AOI around the selected
    longitude and latitude.

    Returns the pixel array and metadata.
    """

    min_lon = longitude - buffer_degrees
    min_lat = latitude - buffer_degrees

    max_lon = longitude + buffer_degrees
    max_lat = latitude + buffer_degrees


    with rasterio.open(band_url) as src:

        # Convert WGS84 coordinates to
        # the CRS used by the Sentinel raster
        bounds = transform_bounds(

            "EPSG:4326",

            src.crs,

            min_lon,
            min_lat,
            max_lon,
            max_lat,

            densify_pts=21

        )


        window = from_bounds(

            *bounds,

            transform=src.transform

        )


        window = window.round_offsets().round_lengths()


        data = src.read(

            1,

            window=window,

            boundless=True,

            fill_value=0

        )


        metadata = {

            "crs": str(src.crs),

            "width": data.shape[1],

            "height": data.shape[0],

            "resolution": src.res

        }


    return data, metadata


def calculate_statistics(data):

    valid_data = data[
        data > 0
    ]


    if valid_data.size == 0:

        return {

            "min": None,

            "max": None,

            "mean": None,

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

        "valid_pixels": int(
            valid_data.size
        )

    }