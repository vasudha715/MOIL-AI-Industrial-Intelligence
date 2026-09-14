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


from services.terrain_service import (
    get_elevations
)


# ----------------------------------
# TEST LOCATION
# ----------------------------------

latitude = 21.5

longitude = 85.5


print("\nTESTING TERRAIN SERVICE")


print("\nLOCATION:")

print(
    "Latitude:",
    latitude
)

print(
    "Longitude:",
    longitude
)


# ----------------------------------
# GET ELEVATION
# ----------------------------------

elevations = get_elevations(

    [latitude],

    [longitude]

)


# ----------------------------------
# DISPLAY RESULT
# ----------------------------------

print("\nELEVATION:")

print(
    elevations[0],
    "metres"
)


print("\nSUCCESS!")

print(
    "Terrain service is working."
)