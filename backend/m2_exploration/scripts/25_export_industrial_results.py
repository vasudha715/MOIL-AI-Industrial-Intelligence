import sys

from pathlib import Path


# ==========================================
# PROJECT BASE DIRECTORY
# ==========================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


sys.path.append(
    str(BASE_DIR)
)


# ==========================================
# IMPORT INDUSTRIAL ENGINE
# ==========================================

from engine.industrial_analysis_engine import (
    analyze_industrial_area
)


# ==========================================
# IMPORT EXPORT SERVICE
# ==========================================

from services.result_export_service import (
    export_industrial_results
)


# ==========================================
# RUN INDUSTRIAL ANALYSIS
# ==========================================

print(
    "\nRUNNING INDUSTRIAL ANALYSIS..."
)


result = analyze_industrial_area(

    location_name="Keonjhar, Odisha",

    buffer_degrees=0.01,

    grid_rows=10,

    grid_cols=10

)


# ==========================================
# EXPORT RESULTS
# ==========================================

export_paths = export_industrial_results(
    result
)


# ==========================================
# FINAL MESSAGE
# ==========================================

print(
    "\nFILES CREATED SUCCESSFULLY:"
)


for name, path in export_paths.items():

    print(
        f"{name}: {path}"
    )