"""
MOIL AI - Weather Intelligence Service

Purpose:
    Get current weather information for the exploration location.

Important:
    External weather services can temporarily return HTTP 429
    (Too Many Requests). A weather failure must NOT stop the
    complete MOIL AI exploration analysis.

Therefore this service:
    1. Tries Open-Meteo.
    2. Uses real weather when available.
    3. Uses safe fallback weather when the API is unavailable,
       rate-limited, or returns invalid data.
"""

import requests


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def _fallback_weather():
    """
    Safe fallback weather values.

    These values are used only when the external weather service
    cannot be reached.

    The fallback allows the rest of the exploration pipeline to
    continue instead of failing.
    """

    return {
        "temperature": 25.0,
        "humidity": 70.0,
        "rain": 0.0,
        "wind_speed": 10.0,
        "source": "fallback",
    }


def get_weather(latitude, longitude):
    """
    Get current weather for a latitude/longitude.

    External API failure is intentionally handled here so that
    weather availability never becomes a hard dependency for
    exploration analysis.
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "wind_speed_10m"
        ),
        "timezone": "auto",
    }

    try:
        response = requests.get(
            OPEN_METEO_URL,
            params=params,
            timeout=10,
        )

        # ---------------------------------------------------------
        # RATE LIMIT
        # ---------------------------------------------------------

        if response.status_code == 429:
            print(
                "Open-Meteo rate limit reached. "
                "Using fallback weather data."
            )

            return _fallback_weather()

        # ---------------------------------------------------------
        # OTHER HTTP ERRORS
        # ---------------------------------------------------------

        if not response.ok:
            print(
                f"Open-Meteo returned HTTP "
                f"{response.status_code}. "
                "Using fallback weather data."
            )

            return _fallback_weather()

        # ---------------------------------------------------------
        # JSON RESPONSE
        # ---------------------------------------------------------

        data = response.json()

        current = data.get("current")

        if not current:
            print(
                "Open-Meteo returned no current weather data. "
                "Using fallback weather data."
            )

            return _fallback_weather()

        temperature = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        rain = current.get("precipitation")
        wind_speed = current.get("wind_speed_10m")

        # ---------------------------------------------------------
        # VALIDATION
        # ---------------------------------------------------------

        if temperature is None:
            temperature = 25.0

        if humidity is None:
            humidity = 70.0

        if rain is None:
            rain = 0.0

        if wind_speed is None:
            wind_speed = 10.0

        weather = {
            "temperature": float(temperature),
            "humidity": float(humidity),
            "rain": float(rain),
            "wind_speed": float(wind_speed),
            "source": "open-meteo",
        }

        print("Weather data loaded successfully.")
        print("Weather:", weather)

        return weather

    # -------------------------------------------------------------
    # NETWORK / REQUEST ERROR
    # -------------------------------------------------------------

    except requests.exceptions.RequestException as error:

        print(
            "Weather service unavailable. "
            "Using fallback weather data."
        )

        print("Weather error:", error)

        return _fallback_weather()

    # -------------------------------------------------------------
    # JSON / UNEXPECTED ERROR
    # -------------------------------------------------------------

    except Exception as error:

        print(
            "Unexpected weather service error. "
            "Using fallback weather data."
        )

        print("Weather error:", error)

        return _fallback_weather()