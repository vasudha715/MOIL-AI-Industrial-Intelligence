from geopy.geocoders import Nominatim
from geopy.exc import (
    GeocoderTimedOut,
    GeocoderUnavailable
)


# ==========================================
# LOCATION SEARCH
# ==========================================

def search_location(location_name):

    # --------------------------------------
    # CREATE GEOCODER
    # --------------------------------------

    geolocator = Nominatim(
        user_agent="moil_ai_exploration_system",
        timeout=10
    )


    # --------------------------------------
    # TRY ONLINE LOCATION SEARCH
    # --------------------------------------

    try:

        location = geolocator.geocode(
            location_name,
            timeout=10
        )


        if location is not None:

            return {

                "name": location.address,

                "latitude": round(
                    location.latitude,
                    6
                ),

                "longitude": round(
                    location.longitude,
                    6
                )

            }


    except (
        GeocoderTimedOut,
        GeocoderUnavailable
    ) as error:

        print(
            "\nWARNING: ONLINE LOCATION "
            "SERVICE IS TEMPORARILY "
            "UNAVAILABLE."
        )

        print(
            "Using available fallback "
            "location data..."
        )


    # --------------------------------------
    # FALLBACK LOCATIONS
    # --------------------------------------

    fallback_locations = {

        "keonjhar, odisha": {

            "name":
                "Keonjhar, Kendujhar, Odisha, India",

            "latitude":
                21.6289,

            "longitude":
                85.5815

        },


        "keonjhar": {

            "name":
                "Keonjhar, Kendujhar, Odisha, India",

            "latitude":
                21.6289,

            "longitude":
                85.5815

        },


        "kendujhar, odisha": {

            "name":
                "Keonjhar, Kendujhar, Odisha, India",

            "latitude":
                21.6289,

            "longitude":
                85.5815

        }

    }


    # --------------------------------------
    # CHECK FALLBACK
    # --------------------------------------

    normalized_name = (
        location_name
        .strip()
        .lower()
    )


    if normalized_name in fallback_locations:

        return (
            fallback_locations[
                normalized_name
            ]
        )


    # --------------------------------------
    # LOCATION NOT FOUND
    # --------------------------------------

    raise ValueError(

        f"Location could not be found: "
        f"{location_name}"

    )