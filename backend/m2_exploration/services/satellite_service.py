from pystac_client import Client


STAC_URL = (
    "https://planetarycomputer.microsoft.com/api/stac/v1"
)


def search_sentinel2(
    longitude,
    latitude,
    buffer_degrees=0.02,
    start_date="2024-01-01",
    end_date="2026-12-31",
    max_cloud_cover=20
):

    catalog = Client.open(
        STAC_URL
    )


    bbox = [

        longitude - buffer_degrees,
        latitude - buffer_degrees,

        longitude + buffer_degrees,
        latitude + buffer_degrees

    ]


    search = catalog.search(

        collections=[
            "sentinel-2-l2a"
        ],

        bbox=bbox,

        datetime=(
            f"{start_date}/{end_date}"
        ),

        query={

            "eo:cloud_cover": {

                "lt": max_cloud_cover

            }

        }

    )


    items = list(
        search.items()
    )


    return items


def select_best_image(items):

    if not items:

        return None


    sorted_items = sorted(

        items,

        key=lambda item:

        item.properties.get(
            "eo:cloud_cover",
            100
        )

    )


    return sorted_items[0]