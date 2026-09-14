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
    read_band_aoi
)

from services.spectral_service import (
    calculate_spectral_features
)

from services.grid_service import (
    create_grid_features
)


# ---------------------------------------
# LOCATION
# ---------------------------------------

location = search_location(
    "Keonjhar, Odisha, India"
)

latitude = location["latitude"]
longitude = location["longitude"]


print("\nLOCATION:")

print(location["name"])


# ---------------------------------------
# SATELLITE SEARCH
# ---------------------------------------

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

print(best_image.id)


# ---------------------------------------
# BAND ASSETS
# ---------------------------------------

band_assets = get_band_assets(
    best_image
)


# ---------------------------------------
# READ BANDS
# ---------------------------------------

bands = {}


required_bands = [

    "B02",
    "B03",
    "B04",
    "B08",
    "B11",
    "B12"

]


print("\nREADING BANDS...")


for band_name in required_bands:

    data, metadata = read_band_aoi(

        band_assets[band_name],

        longitude,

        latitude

    )

    bands[band_name] = data

    print(
        f"{band_name}: {data.shape}"
    )


# ---------------------------------------
# SPECTRAL FEATURES
# ---------------------------------------

print(
    "\nCALCULATING FEATURES..."
)


features = calculate_spectral_features(
    bands
)


# ---------------------------------------
# CREATE GRID
# ---------------------------------------

print(
    "\nCREATING EXPLORATION GRID..."
)


grid = create_grid_features(

    features,

    latitude,

    longitude,

    grid_rows=10,

    grid_cols=10,

    buffer_degrees=0.01

)


# ---------------------------------------
# DISPLAY
# ---------------------------------------

print(
    "\nTOTAL ZONES:"
)

print(
    len(grid)
)


print(
    "\nFIRST 10 ZONES:"
)


print(
    grid.head(10)
)


# ---------------------------------------
# SAVE DATA
# ---------------------------------------

output_path = (

    BASE_DIR
    / "data"
    / "processed"
    / "exploration_grid.csv"

)


grid.to_csv(

    output_path,

    index=False
)


print(
    "\nSAVED:"
)

print(
    output_path
)


print(
    "\nSUCCESS!"
)

print(
    "Exploration grid generated."
)