import sys

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))


from services.aoi_service import search_location

from services.weather_service import get_weather


location = search_location(
    "Keonjhar, Odisha, India"
)


weather = get_weather(

    location["latitude"],

    location["longitude"]

)


print("\nLOCATION:")

print(location["name"])


print("\nWEATHER:")

print(weather["current"])