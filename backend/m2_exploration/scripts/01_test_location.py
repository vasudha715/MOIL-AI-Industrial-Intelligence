import sys

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))


from services.aoi_service import search_location


location = search_location(
    "Keonjhar, Odisha, India"
)


print(location)