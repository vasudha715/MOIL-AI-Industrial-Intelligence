import numpy as np
import pandas as pd


def create_grid_features(
    features,
    latitude,
    longitude,
    grid_rows=10,
    grid_cols=10,
    buffer_degrees=0.01
):
    """
    Divide the selected AOI into a spatial grid.

    Each zone contains:

    - Zone ID
    - Grid row and column
    - Geographic boundaries
    - Center latitude
    - Center longitude
    - Average satellite-derived features
    """


    # ----------------------------------
    # GET FEATURE DIMENSIONS
    # ----------------------------------

    first_feature = list(
        features.values()
    )[0]


    height, width = first_feature.shape


    # ----------------------------------
    # CREATE PIXEL GRID
    # ----------------------------------

    row_edges = np.linspace(

        0,
        height,
        grid_rows + 1,
        dtype=int

    )


    col_edges = np.linspace(

        0,
        width,
        grid_cols + 1,
        dtype=int

    )


    # ----------------------------------
    # CREATE GEOGRAPHIC AOI
    # ----------------------------------

    min_lat = (
        latitude - buffer_degrees
    )


    max_lat = (
        latitude + buffer_degrees
    )


    min_lon = (
        longitude - buffer_degrees
    )


    max_lon = (
        longitude + buffer_degrees
    )


    # ----------------------------------
    # CREATE GEOGRAPHIC GRID EDGES
    # ----------------------------------

    lat_edges = np.linspace(

        max_lat,
        min_lat,
        grid_rows + 1

    )


    lon_edges = np.linspace(

        min_lon,
        max_lon,
        grid_cols + 1

    )


    # ----------------------------------
    # STORE ZONES
    # ----------------------------------

    zones = []

    zone_number = 1


    # ----------------------------------
    # CREATE EACH ZONE
    # ----------------------------------

    for row in range(grid_rows):

        for col in range(grid_cols):


            # --------------------------
            # PIXEL BOUNDARIES
            # --------------------------

            row_start = (
                row_edges[row]
            )


            row_end = (
                row_edges[row + 1]
            )


            col_start = (
                col_edges[col]
            )


            col_end = (
                col_edges[col + 1]
            )


            # --------------------------
            # GEOGRAPHIC BOUNDARIES
            # --------------------------

            zone_max_lat = (
                lat_edges[row]
            )


            zone_min_lat = (
                lat_edges[row + 1]
            )


            zone_min_lon = (
                lon_edges[col]
            )


            zone_max_lon = (
                lon_edges[col + 1]
            )


            # --------------------------
            # CENTER COORDINATES
            # --------------------------

            center_lat = (

                zone_min_lat
                +
                zone_max_lat

            ) / 2


            center_lon = (

                zone_min_lon
                +
                zone_max_lon

            ) / 2


            # --------------------------
            # CREATE ZONE
            # --------------------------

            zone = {

                "zone_id":

                    f"ZONE_{zone_number:03d}",


                "grid_row":

                    row,


                "grid_col":

                    col,


                "center_lat":

                    float(center_lat),


                "center_lon":

                    float(center_lon),


                "min_lat":

                    float(zone_min_lat),


                "max_lat":

                    float(zone_max_lat),


                "min_lon":

                    float(zone_min_lon),


                "max_lon":

                    float(zone_max_lon)

            }


            # --------------------------
            # CALCULATE FEATURES
            # --------------------------

            for feature_name, data in features.items():


                cell = data[

                    row_start:row_end,

                    col_start:col_end

                ]


                valid_values = cell[

                    np.isfinite(cell)

                ]


                if valid_values.size > 0:


                    zone[feature_name] = (

                        float(
                            np.mean(
                                valid_values
                            )
                        )

                    )


                else:


                    zone[feature_name] = None


            # --------------------------
            # ADD ZONE
            # --------------------------

            zones.append(
                zone
            )


            zone_number += 1


    # ----------------------------------
    # RETURN DATAFRAME
    # ----------------------------------

    return pd.DataFrame(
        zones
    )