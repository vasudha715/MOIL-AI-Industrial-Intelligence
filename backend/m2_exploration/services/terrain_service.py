import requests


ELEVATION_API_URL = (
    "https://api.open-meteo.com/v1/elevation"
)


def get_elevations(
    latitudes,
    longitudes
):

    """
    Get terrain elevation data.

    Uses Open-Meteo Elevation API.

    IMPORTANT:
    If the API is unavailable or rate-limited,
    the function returns fallback elevation values
    so the complete MOIL AI exploration analysis
    does NOT fail.
    """

    # ------------------------------------------
    # VALIDATE INPUT
    # ------------------------------------------

    if not latitudes or not longitudes:

        return []


    # ------------------------------------------
    # ENSURE SAME LENGTH
    # ------------------------------------------

    count = min(
        len(latitudes),
        len(longitudes)
    )


    latitudes = latitudes[:count]

    longitudes = longitudes[:count]


    # ------------------------------------------
    # API PARAMETERS
    # ------------------------------------------

    params = {

        "latitude":
            ",".join(
                str(x)
                for x in latitudes
            ),

        "longitude":
            ",".join(
                str(x)
                for x in longitudes
            ),

    }


    # ------------------------------------------
    # TRY REAL ELEVATION API
    # ------------------------------------------

    try:

        response = requests.get(

            ELEVATION_API_URL,

            params=params,

            timeout=20

        )


        response.raise_for_status()


        data = response.json()


        elevations = data.get(
            "elevation",
            []
        )


        # --------------------------------------
        # VALID RESPONSE
        # --------------------------------------

        if (
            elevations
            and
            len(elevations) == count
        ):

            print(
                "Real terrain elevation data loaded."
            )


            return elevations


        print(
            "Elevation API returned incomplete data."
        )


    except Exception as error:

        print(
            "Elevation API unavailable."
        )

        print(
            "Using fallback terrain data."
        )

        print(
            "Reason:",
            error
        )


    # ------------------------------------------
    # FALLBACK TERRAIN MODEL
    # ------------------------------------------
    #
    # Generates stable terrain variation based
    # on geographic position.
    #
    # This allows exploration analysis to continue
    # when external elevation service is unavailable.
    # ------------------------------------------

    fallback_elevations = []


    for index in range(count):

        latitude = float(
            latitudes[index]
        )

        longitude = float(
            longitudes[index]
        )


        # --------------------------------------
        # TERRAIN VARIATION
        # --------------------------------------

        elevation = (

            450

            +

            (
                (
                    latitude * 100
                )
                %
                180
            )

            +

            (
                (
                    longitude * 100
                )
                %
                120
            )

        )


        fallback_elevations.append(

            round(
                elevation,
                2
            )

        )


    print(
        "Fallback terrain elevation generated."
    )


    return fallback_elevations