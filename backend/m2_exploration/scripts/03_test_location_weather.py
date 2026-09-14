import sys

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))


from services.aoi_service import search_location

from services.weather_service import get_weather

from services.weather_risk import calculate_weather_risk


location = search_location(
    "Keonjhar, Odisha, India"
)


weather = get_weather(

    location["latitude"],

    location["longitude"]

)


risk = calculate_weather_risk(
    weather
)


print("\nLOCATION")

print(location)


print("\nCURRENT WEATHER")

print(weather["current"])


print("\nWEATHER RISK")

print(risk)