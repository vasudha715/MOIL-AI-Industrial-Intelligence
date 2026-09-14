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


location = search_location(
    "Keonjhar, Odisha, India"
)


print("\nLOCATION:")

print(
    location["name"]
)


items = search_sentinel2(

    longitude=location["longitude"],

    latitude=location["latitude"],

    max_cloud_cover=20

)


best_image = select_best_image(
    items
)


if best_image is None:

    print(
        "No suitable image found."
    )

    exit()


print("\nBEST IMAGE:")

print(
    best_image.id
)


bands = get_band_assets(
    best_image
)


print("\nAVAILABLE REQUIRED BANDS:\n")


for band, url in bands.items():

    print(
        f"{band}:"
    )

    print(
        url[:120] + "..."
    )

    print()