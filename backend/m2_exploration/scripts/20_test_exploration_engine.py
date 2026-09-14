import sys
import os


# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)


from engine.exploration_engine import (
    analyze_area
)


result = analyze_area(

    location_name="Keonjhar",

    buffer_degrees=0.01,

    grid_rows=10,

    grid_cols=10

)


print("\n======================================")
print("FINAL RESULT SUMMARY")
print("======================================")


print("\nLOCATION:")

print(
    result["location"]
)


print("\nWEATHER:")

print(
    result["weather"]
)


print("\nWEATHER RISK:")

print(
    result["weather_risk"]
)


print("\nSATELLITE:")

print(
    result["satellite"]
)


print("\nTOTAL EXPLORATION ZONES:")

print(
    len(
        result["exploration_grid"]
    )
)


print("\nFIRST 5 ZONES:")

print(

    result[
        "exploration_grid"
    ].head()

)