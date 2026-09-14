"""
Production & Risk Service (M3).

Provides:
- Historical production data
- Dynamic yearly production forecasts
- Production summary
- Target vs forecast shortfall analysis
- Production risk alerts

Forecasting method:
Seasonal Naive

The forecast year is generated dynamically using the latest
available historical production year.
"""

import csv
from pathlib import Path
from typing import List, Dict, Optional

from sqlalchemy.orm import Session

import models


DATA_DIR = Path(__file__).resolve().parent / "data"


# =========================================================
# HISTORICAL PRODUCTION DATA
# =========================================================

def load_history() -> List[Dict]:
    """
    Load historical production data from CSV.
    """

    path = DATA_DIR / "production_history.csv"

    rows = []

    with open(
        path,
        newline="",
        encoding="utf-8-sig"
    ) as f:

        reader = csv.DictReader(f)

        for r in reader:

            rows.append({

                "month": r["Month"],

                "production_tonnes": float(
                    r["Production (tonnes)"]
                ),

                "state": r["State"],

                "source": r["Source"],

                "data_quality": r["Data Quality"],

            })

    return rows


# =========================================================
# AVAILABLE HISTORICAL YEARS
# =========================================================

def get_available_years() -> List[int]:
    """
    Return all years available in the historical dataset.
    """

    years = set()

    for row in load_history():

        year = int(
            row["month"].split("-")[0]
        )

        years.add(year)

    return sorted(years)


# =========================================================
# LATEST HISTORICAL YEAR
# =========================================================

def get_latest_historical_year() -> int:
    """
    Return the latest year available in historical data.
    """

    years = get_available_years()

    if not years:

        raise ValueError(
            "No historical production data available."
        )

    return max(years)


# =========================================================
# DEFAULT FORECAST YEAR
# =========================================================

def get_default_forecast_year() -> int:
    """
    Forecast the year immediately after the latest
    historical production year.
    """

    return get_latest_historical_year() + 1


# =========================================================
# DYNAMIC FORECAST ENGINE
# =========================================================

def generate_dynamic_forecast(
    forecast_year: Optional[int] = None
) -> List[Dict]:
    """
    Generate a dynamic 12-month production forecast.

    Method:
    Seasonal Naive

    Example:

    Latest historical year:
    2025

    Forecast year:
    2026

    January 2026 forecast
    =
    January 2025 production

    February 2026 forecast
    =
    February 2025 production
    """

    history = load_history()

    latest_year = (
        get_latest_historical_year()
    )

    if forecast_year is None:

        forecast_year = (
            get_default_forecast_year()
        )

    latest_year_data = {}

    for row in history:

        year, month_number = (
            row["month"].split("-")
        )

        if int(year) == latest_year:

            latest_year_data[
                int(month_number)
            ] = row["production_tonnes"]

    forecast = []

    for month_number in range(1, 13):

        source_value = (
            latest_year_data.get(
                month_number
            )
        )

        if source_value is None:

            continue

        forecast.append({

            "month": (
                f"{forecast_year}-"
                f"{month_number:02d}"
            ),

            "forecast_tonnes": round(
                source_value,
                2
            ),

            "method": (
                "Seasonal Naive"
            ),

            "basis": (
                f"Same calendar month "
                f"in {latest_year}"
            ),

        })

    return forecast


# =========================================================
# FORECAST API FUNCTION
# =========================================================

def load_forecast(
    forecast_year: Optional[int] = None
) -> List[Dict]:
    """
    Public forecast function.

    Generates the forecast dynamically.
    """

    return generate_dynamic_forecast(
        forecast_year
    )


# =========================================================
# PRODUCTION SUMMARY
# =========================================================

def summary(
    forecast_year: Optional[int] = None
) -> Dict:
    """
    Return production summary and forecast information.
    """

    history = load_history()

    available_years = (
        get_available_years()
    )

    latest_year = (
        get_latest_historical_year()
    )

    previous_year = None

    if len(available_years) >= 2:

        previous_year = (
            available_years[-2]
        )

    latest_year_total = sum(

        row["production_tonnes"]

        for row in history

        if row["month"].startswith(
            str(latest_year)
        )

    )

    previous_year_total = None

    if previous_year is not None:

        previous_year_total = sum(

            row["production_tonnes"]

            for row in history

            if row["month"].startswith(
                str(previous_year)
            )

        )

    growth_pct = None

    if (
        previous_year_total
        and previous_year_total != 0
    ):

        growth_pct = (

            (
                latest_year_total
                -
                previous_year_total
            )

            /
            previous_year_total

        ) * 100

    forecast = load_forecast(
        forecast_year
    )

    if forecast_year is None:

        forecast_year = (
            get_default_forecast_year()
        )

    forecast_total = sum(

        row["forecast_tonnes"]

        for row in forecast

    )

    peak = max(

        history,

        key=lambda row:
        row["production_tonnes"]

    )

    return {

        "available_historical_years":
        available_years,

        "latest_historical_year":
        latest_year,

        "previous_historical_year":
        previous_year,

        "previous_year_total_tonnes":
        round(
            previous_year_total,
            2
        )

        if previous_year_total
        is not None

        else None,

        "latest_year_total_tonnes":
        round(
            latest_year_total,
            2
        ),

        "growth_latest_vs_previous_pct":
        round(
            growth_pct,
            2
        )

        if growth_pct
        is not None

        else None,

        "forecast_year":
        forecast_year,

        "forecast_total_tonnes":
        round(
            forecast_total,
            2
        ),

        "peak_month":
        peak["month"],

        "peak_month_tonnes":
        peak["production_tonnes"],

        "model": {

            "selected":
            "Seasonal Naive",

            "source_year":
            latest_year,

            "note":
            (
                "Dynamic Seasonal Naive "
                "forecast using the latest "
                "available historical year."
            ),

        },

    }


# =========================================================
# TARGET VS FORECAST
# =========================================================

def shortfall(
    db: Session,
    forecast_year: Optional[int] = None
) -> List[Dict]:
    """
    Compare production forecast against approved targets.
    """

    forecast_rows = load_forecast(
        forecast_year
    )

    forecast = {

        row["month"]:
        row["forecast_tonnes"]

        for row in forecast_rows

    }

    targets = {

        target.month:
        target.target_tonnes

        for target in

        db.query(
            models.ProductionTarget
        ).all()

    }

    results = []

    for (
        month,
        forecast_tonnes

    ) in forecast.items():

        target = targets.get(
            month
        )

        if target is None:

            results.append({

                "month":
                month,

                "forecast_tonnes":
                forecast_tonnes,

                "approved_target_tonnes":
                None,

                "shortfall_tonnes":
                None,

                "status":
                "Target required",

            })

        else:

            shortfall_tonnes = (

                target
                -
                forecast_tonnes

            )

            results.append({

                "month":
                month,

                "forecast_tonnes":
                forecast_tonnes,

                "approved_target_tonnes":
                target,

                "shortfall_tonnes":
                round(
                    shortfall_tonnes,
                    2
                ),

                "status":

                (
                    "At risk of shortfall"

                    if shortfall_tonnes > 0

                    else "On track"
                ),

            })

    return results


# =========================================================
# PRODUCTION ALERTS
# =========================================================

def alerts(
    db: Session,
    forecast_year: Optional[int] = None
) -> List[Dict]:
    """
    Generate production and shortfall alerts.
    """

    out = []

    history = load_history()


    # -----------------------------------------------------
    # MONTH-ON-MONTH PRODUCTION DECLINE
    # -----------------------------------------------------

    for i in range(
        1,
        len(history)
    ):

        previous = history[i - 1]

        current = history[i]


        # Only compare consecutive months
        previous_year = int(
            previous["month"].split("-")[0]
        )

        current_year = int(
            current["month"].split("-")[0]
        )

        previous_month = int(
            previous["month"].split("-")[1]
        )

        current_month = int(
            current["month"].split("-")[1]
        )


        consecutive = (

            (
                current_year == previous_year
                and
                current_month
                ==
                previous_month + 1
            )

            or

            (
                current_year
                ==
                previous_year + 1
                and
                previous_month == 12
                and
                current_month == 1
            )

        )


        if not consecutive:

            continue


        if (
            previous["production_tonnes"]
            == 0
        ):

            continue


        change_pct = (

            (

                current["production_tonnes"]

                -

                previous["production_tonnes"]

            )

            /

            previous["production_tonnes"]

        ) * 100


        if change_pct <= -15:

            out.append({

                "type":
                "Production Drop",

                "severity":

                (
                    "high"

                    if change_pct <= -25

                    else "medium"
                ),

                "message":

                (
                    f"Production fell "

                    f"{abs(round(change_pct, 1))}% "

                    f"in {current['month']} "

                    f"vs {previous['month']}."
                ),

            })


    # -----------------------------------------------------
    # FORECAST SHORTFALL ALERTS
    # -----------------------------------------------------

    for row in shortfall(
        db,
        forecast_year
    ):

        if (

            row["status"]
            ==
            "At risk of shortfall"

        ):

            out.append({

                "type":
                "Shortfall",

                "severity":
                "high",

                "message":

                (
                    f"{row['month']} forecast "

                    f"({row['forecast_tonnes']:.0f}t) "

                    f"is "

                    f"{row['shortfall_tonnes']:.0f}t "

                    f"below the approved target."
                ),

            })


    if not out:

        out.append({

            "type":
            "Info",

            "severity":
            "low",

            "message":

            (
                "No production alerts at "
                "this time."
            ),

        })


    return out


# =========================================================
# SET OR UPDATE PRODUCTION TARGET
# =========================================================

def set_target(
    db: Session,
    month: str,
    target_tonnes: float
) -> models.ProductionTarget:
    """
    Create or update an approved production target.
    """

    existing = (

        db.query(
            models.ProductionTarget
        )

        .filter(

            models.ProductionTarget.month
            ==
            month

        )

        .first()

    )


    if existing:

        existing.target_tonnes = (
            target_tonnes
        )

        db.commit()

        db.refresh(
            existing
        )

        return existing


    target = (

        models.ProductionTarget(

            month=month,

            target_tonnes=target_tonnes

        )

    )


    db.add(
        target
    )

    db.commit()

    db.refresh(
        target
    )

    return target