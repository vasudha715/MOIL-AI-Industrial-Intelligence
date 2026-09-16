import time
import random
import requests


# ==========================================
# USGS MINERAL RESOURCE DATA SYSTEM
# ==========================================

USGS_MRDS_URL = (
    "https://energy.usgs.gov/"
    "arcgis/rest/services/Hosted/"
    "Mineral_Resource_Data_System/"
    "FeatureServer/0/query"
)


# ==========================================
# RETRY SETTINGS
# ==========================================

MAX_RETRIES = 3

BASE_DELAY = 2


# ==========================================
# GET MINERAL OCCURRENCES
# ==========================================

def get_mineral_occurrences(
    min_lat,
    min_lon,
    max_lat,
    max_lon
):
    """
    Retrieve mineral occurrence records
    inside the selected geographic area.

    Returns GeoJSON data from the
    USGS Mineral Resource Data System.

    If the USGS service is temporarily
    unavailable or rate-limited, the
    function returns an empty GeoJSON
    FeatureCollection so the complete
    exploration analysis can continue.
    """

    # --------------------------------------
    # CREATE GEOGRAPHIC BOUNDING BOX
    # --------------------------------------

    geometry = (
        f"{min_lon},"
        f"{min_lat},"
        f"{max_lon},"
        f"{max_lat}"
    )


    # --------------------------------------
    # REQUEST PARAMETERS
    # --------------------------------------

    params = {

        "where": "1=1",

        "geometry": geometry,

        "geometryType":
            "esriGeometryEnvelope",

        "inSR": "4326",

        "spatialRel":
            "esriSpatialRelIntersects",

        "outFields": "*",

        "returnGeometry": "true",

        "f": "geojson"

    }


    # --------------------------------------
    # RETRY USGS REQUEST
    # --------------------------------------

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            print(
                f"USGS occurrence request "
                f"(attempt {attempt}/{MAX_RETRIES})..."
            )


            response = requests.get(

                USGS_MRDS_URL,

                params=params,

                timeout=30

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


                # Add small random jitter
                delay += random.uniform(
                    0.5,
                    1.5
                )


                print(
                    "USGS rate limit reached "
                    "(HTTP 429)."
                )

                print(
                    f"Waiting {delay:.1f} seconds "
                    "before retry..."
                )


                if attempt < MAX_RETRIES:

                    time.sleep(delay)

                    continue


                print(
                    "USGS rate limit persisted."
                )

                print(
                    "Using empty occurrence "
                    "dataset."
                )

                return _empty_geojson()


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
                    f"USGS temporary server error: "
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
                    "USGS service did not recover."
                )

                print(
                    "Using empty occurrence "
                    "dataset."
                )

                return _empty_geojson()


            # ----------------------------------
            # OTHER HTTP ERRORS
            # ----------------------------------

            response.raise_for_status()


            # ----------------------------------
            # PARSE RESPONSE
            # ----------------------------------

            data = response.json()


            # ----------------------------------
            # VALIDATE GEOJSON
            # ----------------------------------

            if isinstance(data, dict):

                if data.get("type") == "FeatureCollection":

                    print(
                        "USGS mineral occurrence "
                        "data loaded successfully."
                    )


                    features = data.get(
                        "features",
                        []
                    )


                    print(
                        f"USGS occurrence records: "
                        f"{len(features)}"
                    )


                    return data


            print(
                "USGS returned an unexpected "
                "response format."
            )


            return _empty_geojson()


        # --------------------------------------
        # NETWORK / TIMEOUT ERRORS
        # --------------------------------------

        except requests.exceptions.Timeout as error:

            print(
                "USGS occurrence request timed out."
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
                "USGS timeout persisted."
            )

            print(
                "Using empty occurrence dataset."
            )

            return _empty_geojson()


        except requests.exceptions.RequestException as error:

            print(
                "USGS occurrence service error:"
            )

            print(error)


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
                "USGS service unavailable."
            )

            print(
                "Using empty occurrence dataset."
            )

            return _empty_geojson()


        except Exception as error:

            print(
                "Unexpected USGS occurrence error:"
            )

            print(error)


            return _empty_geojson()


    # --------------------------------------
    # FINAL SAFETY FALLBACK
    # --------------------------------------

    return _empty_geojson()


# ==========================================
# EMPTY GEOJSON FALLBACK
# ==========================================

def _empty_geojson():

    return {

        "type": "FeatureCollection",

        "features": []

    }