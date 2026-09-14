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


from services.aoi_service import search_location

from services.satellite_service import (
    search_sentinel2
)


location = search_location(
    "Keonjhar, Odisha, India"
)


items = search_sentinel2(

    longitude=location["longitude"],

    latitude=location["latitude"]

)


print("\nLOCATION:")

print(location["name"])


print("\nSATELLITE IMAGES FOUND:")

print(len(items))


for item in items:

    print("\nID:")

    print(item.id)


    print("DATE:")

    print(
        item.properties.get(
            "datetime"
        )
    )


    print("CLOUD COVER:")

    print(
        item.properties.get(
            "eo:cloud_cover"
        )
    )