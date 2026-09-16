import time
import random
import requests


ELEVATION_API_URL = (
    "https://api.open-meteo.com/v1/elevation"
)


# ==========================================
# RETRY SETTINGS
# ==========================================

MAX_RETRIES = 3

BASE_DELAY = 2


# ==========================================
# FALLBACK ELEVATION
# ==========================================

def _fallback_elevations(
    latitudes,
    longitudes
):

    fallback_elevations = []


    for index in range(
        len(latitudes)
    ):

        latitude = float(
            latitudes[index]
        )

        longitude = float(
            longitudes[index]
        )


        # Stable terrain variation
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


# ==========================================
# GET ELEVATIONS
# ==========================================

def get_elevations(
    latitudes,
    longitudes
):

    """
    Get terrain elevation data.

    Uses Open-Meteo Elevation API.

    Includes retry/backoff handling for
    temporary API failures and HTTP 429.

    If the API remains unavailable,
    deterministic fallback elevation values
    are returned so exploration analysis
    can continue.
    """

    # --------------------------------------
    # VALIDATE INPUT
    # --------------------------------------

    if not latitudes or not longitudes:

        return []


    # --------------------------------------
    # ENSURE SAME LENGTH
    # --------------------------------------

    count = min(
        len(latitudes),
        len(longitudes)
    )


    latitudes = latitudes[:count]

    longitudes = longitudes[:count]


    # --------------------------------------
    # API PARAMETERS
    # --------------------------------------

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


    # --------------------------------------
    # TRY REAL ELEVATION API
    # --------------------------------------

    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):

        try:

            print(
                f"Elevation API request "
                f"(attempt {attempt}/{MAX_RETRIES})..."
            )


            response = requests.get(

                ELEVATION_API_URL,

                params=params,

                timeout=20

            )


            # ----------------------------------
            # RATE LIMIT
            # ----------------------------------

            if response.status_code == 429:

                retry_after = response.headers.get(
                    "Retry-After"
                )


                if retry_after:

                    try:

                        delay = float(
                            retry_after
                        )

                    except ValueError:

                        delay = (
                            BASE_DELAY
                            * (2 ** (attempt - 1))
                        )

                else:

                    delay = (
                        BASE_DELAY
                        * (2 ** (attempt - 1))
                    )


                delay += random.uniform(
                    0.5,
                    1.5
                )


                print(
                    "Elevation API rate limit "
                    "reached (HTTP 429)."
                )


                if attempt < MAX_RETRIES:

                    print(
                        f"Retrying in "
                        f"{delay:.1f} seconds..."
                    )

                    time.sleep(delay)

                    continue


                print(
                    "Elevation API rate limit "
                    "persisted."
                )

                print(
                    "Using fallback terrain data."
                )

                break


            # ----------------------------------
            # TEMPORARY SERVER ERRORS
            # ----------------------------------

            if response.status_code in (
                500,
                502,
                503,
                504
            ):

                print(
                    f"Elevation API temporary "
                    f"server error: "
                    f"HTTP {response.status_code}"
                )


                if attempt < MAX_RETRIES:

                    delay = (
                        BASE_DELAY
                        * (2 ** (attempt - 1))
                    )

                    delay += random.uniform(
                        0.5,
                        1.5
                    )


                    print(
                        f"Retrying in "
                        f"{delay:.1f} seconds..."
                    )


                    time.sleep(delay)

                    continue


                print(
                    "Elevation API did not recover."
                )

                print(
                    "Using fallback terrain data."
                )

                break


            # ----------------------------------
            # OTHER HTTP ERRORS
            # ----------------------------------

            response.raise_for_status()


            # ----------------------------------
            # PARSE RESPONSE
            # ----------------------------------

            data = response.json()


            elevations = data.get(
                "elevation",
                []
            )


            # ----------------------------------
            # VALID RESPONSE
            # ----------------------------------

            if (
                elevations
                and
                len(elevations) == count
            ):

                print(
                    "Real terrain elevation "
                    "data loaded."
                )


                return elevations


            print(
                "Elevation API returned "
                "incomplete data."
            )


            break


        # --------------------------------------
        # TIMEOUT
        # --------------------------------------

        except requests.exceptions.Timeout as error:

            print(
                "Elevation API request timed out."
            )

            print(
                "Reason:",
                error
            )


            if attempt < MAX_RETRIES:

                delay = (
                    BASE_DELAY
                    * (2 ** (attempt - 1))
                )

                delay += random.uniform(
                    0.5,
                    1.5
                )


                print(
                    f"Retrying in "
                    f"{delay:.1f} seconds..."
                )


                time.sleep(delay)

                continue


            print(
                "Elevation API timeout persisted."
            )

            break


        # --------------------------------------
        # NETWORK ERROR
        # --------------------------------------

        except requests.exceptions.RequestException as error:

            print(
                "Elevation API unavailable."
            )

            print(
                "Reason:",
                error
            )


            if attempt < MAX_RETRIES:

                delay = (
                    BASE_DELAY
                    * (2 ** (attempt - 1))
                )

                delay += random.uniform(
                    0.5,
                    1.5
                )


                print(
                    f"Retrying in "
                    f"{delay:.1f} seconds..."
                )


                time.sleep(delay)

                continue


            break


        # --------------------------------------
        # UNEXPECTED ERROR
        # --------------------------------------

        except Exception as error:

            print(
                "Unexpected elevation "
                "service error."
            )

            print(
                "Reason:",
                error
            )

            break


    # ------------------------------------------
    # FALLBACK TERRAIN MODEL
    # ------------------------------------------

    print(
        "Using fallback terrain data."
    )


    return _fallback_elevations(
        latitudes,
        longitudes
    )