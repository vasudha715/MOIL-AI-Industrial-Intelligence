def calculate_weather_risk(weather):

    current = weather.get("current", {})

    rain = current.get("rain", 0)

    wind = current.get("wind_speed_10m", 0)


    if rain >= 10:

        return {
            "risk": "HIGH",
            "score": 80,
            "message":
                "Heavy rainfall may affect exploration and field operations."
        }


    elif rain >= 2:

        return {
            "risk": "MODERATE",
            "score": 50,
            "message":
                "Rainfall may cause delays in field activities."
        }


    elif wind >= 40:

        return {
            "risk": "MODERATE",
            "score": 55,
            "message":
                "High wind may affect outdoor operations."
        }


    else:

        return {
            "risk": "LOW",
            "score": 20,
            "message":
                "Current weather conditions are generally suitable for field work."
        }