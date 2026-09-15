import requests


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

    # ==========================================
    # TRY LIVE WEATHER API
    # ==========================================

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        # Successful response
        if response.status_code == 200:

            data = response.json()

            data["fallback"] = False

            return data

        # ======================================
        # RATE LIMIT
        # ======================================

        if response.status_code == 429:

            print(
                "Open-Meteo rate limit reached."
            )

            print(
                "Using fallback weather data."
            )

            return get_fallback_weather()

        # ======================================
        # OTHER HTTP ERROR
        # ======================================

        response.raise_for_status()

    except requests.RequestException as error:

        print(
            f"Weather API unavailable: {error}"
        )

        print(
            "Using fallback weather data."
        )

        return get_fallback_weather()


# ==========================================
# FALLBACK WEATHER
# ==========================================

def get_fallback_weather():

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