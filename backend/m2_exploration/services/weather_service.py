import requests
import time


def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "rain",
            "wind_speed_10m"
        ],

        "daily": [
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max"
        ],

        "forecast_days": 3,

        "timezone": "auto"
    }

    # Try live weather API
    for attempt in range(3):

        try:

            response = requests.get(
                url,
                params=params,
                timeout=20
            )

            if response.status_code == 200:
                return response.json()

            # Rate limit
            if response.status_code == 429:

                print(
                    "Weather API rate limit reached. Retrying..."
                )

                time.sleep(2 * (attempt + 1))

                continue

            response.raise_for_status()

        except requests.RequestException as error:

            print(
                f"Weather API attempt {attempt + 1} failed: {error}"
            )

            time.sleep(2 * (attempt + 1))

    # Fallback weather data
    print(
        "Using fallback weather data. "
        "Live weather API is temporarily unavailable."
    )

    return {
        "current": {
            "temperature_2m": 27.0,
            "relative_humidity_2m": 70,
            "rain": 0.0,
            "wind_speed_10m": 12.0
        },

        "daily": {
            "precipitation_sum": [
                0.0,
                1.2,
                0.5
            ],

            "precipitation_probability_max": [
                20,
                35,
                25
            ],

            "wind_speed_10m_max": [
                15.0,
                18.0,
                14.0
            ]
        },

        "fallback": True
    }