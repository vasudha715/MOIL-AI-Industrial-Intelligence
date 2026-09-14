import requests


ELEVATION_API_URL = (
    "https://api.open-meteo.com/v1/elevation"
)


def get_elevations(
    latitudes,
    longitudes
):
    """
    Get real terrain elevation data
    from the Open-Meteo Elevation API.

    Parameters:
        latitudes: list of latitude values
        longitudes: list of longitude values

    Returns:
        List of elevation values in metres.
    """

    if len(latitudes) != len(longitudes):

        raise ValueError(
            "Latitude and longitude counts "
            "must be equal."
        )


    latitude_string = ",".join(
        str(latitude)
        for latitude in latitudes
    )


    longitude_string = ",".join(
        str(longitude)
        for longitude in longitudes
    )


    parameters = {

        "latitude":
            latitude_string,

        "longitude":
            longitude_string

    }


    try:

        response = requests.get(

            ELEVATION_API_URL,

            params=parameters,

            timeout=30

        )


        response.raise_for_status()


        data = response.json()


        if "elevation" not in data:

            raise ValueError(
                "Elevation data was not "
                "returned by the API."
            )


        elevations = data[
            "elevation"
        ]


        if len(elevations) != len(latitudes):

            raise ValueError(
                "Number of returned elevations "
                "does not match input coordinates."
            )


        return elevations


    except requests.RequestException as error:

        print(
            "\nERROR CONNECTING TO "
            "ELEVATION API:"
        )

        print(error)

        raise