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
    # CALL USGS SERVICE
    # --------------------------------------

    try:

        response = requests.get(

            USGS_MRDS_URL,

            params=params,

            timeout=60

        )


        response.raise_for_status()


        data = response.json()


        return data


    except requests.exceptions.RequestException as error:

        print(
            "\nERROR CONNECTING TO "
            "USGS OCCURRENCE SERVICE:"
        )

        print(error)


        return None