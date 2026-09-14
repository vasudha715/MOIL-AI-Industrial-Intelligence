import planetary_computer


REQUIRED_BANDS = [

    "B02",
    "B03",
    "B04",
    "B08",
    "B11",
    "B12"

]


def get_band_assets(item):

    signed_item = (
        planetary_computer.sign(item)
    )


    bands = {}


    for band in REQUIRED_BANDS:

        if band in signed_item.assets:

            bands[band] = (
                signed_item.assets[band].href
            )


    return bands