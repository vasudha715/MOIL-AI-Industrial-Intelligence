import numpy as np


def calculate_terrain_features(
    dataframe,
    grid_rows=10,
    grid_cols=10
):
    """
    Calculate terrain slope and terrain roughness
    using elevation values from the exploration grid.

    SLOPE_DEG:
        Approximate terrain slope in degrees.

    TERRAIN_ROUGHNESS_M:
        Standard deviation of elevation in the
        local neighbourhood.
    """

    # ----------------------------------
    # CREATE ELEVATION GRID
    # ----------------------------------

    elevation_grid = np.zeros(
        (grid_rows, grid_cols),
        dtype=np.float32
    )


    for _, row in dataframe.iterrows():

        grid_row = int(
            row["grid_row"]
        )

        grid_col = int(
            row["grid_col"]
        )

        elevation = float(
            row["ELEVATION_M"]
        )


        elevation_grid[
            grid_row,
            grid_col
        ] = elevation


    # ----------------------------------
    # CALCULATE GRID SPACING
    # ----------------------------------

    # Approximate geographic distance
    # between neighboring zone centres.

    first_row = dataframe.iloc[0]


    # Latitude spacing
    lat_spacing_deg = abs(

        dataframe[
            dataframe["grid_col"] == 0
        ]
        .sort_values("grid_row")
        ["center_lat"]
        .iloc[1]

        -

        dataframe[
            dataframe["grid_col"] == 0
        ]
        .sort_values("grid_row")
        ["center_lat"]
        .iloc[0]

    )


    # Longitude spacing
    lon_spacing_deg = abs(

        dataframe[
            dataframe["grid_row"] == 0
        ]
        .sort_values("grid_col")
        ["center_lon"]
        .iloc[1]

        -

        dataframe[
            dataframe["grid_row"] == 0
        ]
        .sort_values("grid_col")
        ["center_lon"]
        .iloc[0]

    )


    # ----------------------------------
    # CONVERT DEGREES TO METRES
    # ----------------------------------

    mean_latitude = float(
        dataframe["center_lat"].mean()
    )


    lat_spacing_m = (
        lat_spacing_deg
        * 111320
    )


    lon_spacing_m = (

        lon_spacing_deg
        * 111320
        * np.cos(
            np.radians(
                mean_latitude
            )
        )

    )


    # ----------------------------------
    # CALCULATE SLOPE
    # ----------------------------------

    gradient_y, gradient_x = np.gradient(

        elevation_grid,

        lat_spacing_m,

        lon_spacing_m

    )


    slope_radians = np.arctan(

        np.sqrt(

            gradient_x ** 2
            +
            gradient_y ** 2

        )

    )


    slope_degrees = np.degrees(
        slope_radians
    )


    # ----------------------------------
    # CALCULATE TERRAIN ROUGHNESS
    # ----------------------------------

    roughness_grid = np.zeros(

        (grid_rows, grid_cols),

        dtype=np.float32

    )


    for row in range(grid_rows):

        for col in range(grid_cols):


            row_start = max(
                0,
                row - 1
            )


            row_end = min(
                grid_rows,
                row + 2
            )


            col_start = max(
                0,
                col - 1
            )


            col_end = min(
                grid_cols,
                col + 2
            )


            neighbourhood = elevation_grid[

                row_start:row_end,

                col_start:col_end

            ]


            roughness_grid[
                row,
                col
            ] = np.std(
                neighbourhood
            )


    # ----------------------------------
    # ADD FEATURES TO DATAFRAME
    # ----------------------------------

    slope_values = []

    roughness_values = []


    for _, row in dataframe.iterrows():

        grid_row = int(
            row["grid_row"]
        )

        grid_col = int(
            row["grid_col"]
        )


        slope_values.append(

            float(

                slope_degrees[
                    grid_row,
                    grid_col
                ]

            )

        )


        roughness_values.append(

            float(

                roughness_grid[
                    grid_row,
                    grid_col
                ]

            )

        )


    dataframe[
        "SLOPE_DEG"
    ] = slope_values


    dataframe[
        "TERRAIN_ROUGHNESS_M"
    ] = roughness_values


    return dataframe