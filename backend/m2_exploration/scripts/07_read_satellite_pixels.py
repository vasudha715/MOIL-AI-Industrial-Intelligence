import sys

from pathlib import Path


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


sys.path.append(
    str(BASE_DIR)
)


from services.aoi_service import (
    search_location
)


from services.satellite_service import (

    search_sentinel2,

    select_best_image

)


from services.band_service import (
    get_band_assets
)


from services.raster_service import (

    read_band_aoi,

    calculate_statistics

)


# ----------------------------------
# SELECT LOCATION
# ----------------------------------

location = search_location(

    "Keonjhar, Odisha, India"

)


longitude = location["longitude"]

latitude = location["latitude"]


print("\nLOCATION:")

print(
    location["name"]
)


print("\nCOORDINATES:")

print(
    latitude,
    longitude
)


# ----------------------------------
# FIND SENTINEL-2 IMAGE
# ----------------------------------

items = search_sentinel2(

    longitude=longitude,

    latitude=latitude,

    max_cloud_cover=20

)


best_image = select_best_image(
    items
)


if best_image is None:

    print(
        "No suitable satellite image found."
    )

    exit()


print("\nBEST IMAGE:")

print(
    best_image.id
)


# ----------------------------------
# GET BAND ASSETS
# ----------------------------------

bands = get_band_assets(
    best_image
)


# ----------------------------------
# READ BANDS
# ----------------------------------

print(
    "\nREADING SATELLITE DATA..."
)


for band_name in [

    "B02",
    "B03",
    "B04",
    "B08",
    "B11",
    "B12"

]:

    print(
        f"\n--- {band_name} ---"
    )


    data, metadata = read_band_aoi(

        bands[band_name],

        longitude,

        latitude

    )


    statistics = calculate_statistics(
        data
    )


    print(
        "Shape:",
        data.shape
    )


    print(
        "Metadata:",
        metadata
    )


    print(
        "Statistics:",
        statistics
    )


print(
    "\nSUCCESS!"
)

print(
    "Satellite pixels were read successfully."
)