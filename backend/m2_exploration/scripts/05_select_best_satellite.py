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


print("\nLOW CLOUD IMAGES FOUND:")

print(
    len(items)
)


best_image = select_best_image(
    items
)


if best_image:

    print("\nBEST IMAGE")

    print(
        "\nID:"
    )

    print(
        best_image.id
    )


    print(
        "\nDATE:"
    )

    print(
        best_image.properties.get(
            "datetime"
        )
    )


    print(
        "\nCLOUD COVER:"
    )

    print(
        best_image.properties.get(
            "eo:cloud_cover"
        )
    )


    print(
        "\nAVAILABLE ASSETS:"
    )

    print(
        list(
            best_image.assets.keys()
        )
    )


else:

    print(
        "\nNo suitable low-cloud "
        "Sentinel-2 image found."
    )