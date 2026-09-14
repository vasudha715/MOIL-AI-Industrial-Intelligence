"""
Production & Risk service (M3).

Converts what used to live only inside M3_Manganese_ALL_WORK_FINAL.xlsx into
live API data: historical production, 2026 forecast, model evaluation,
target-vs-forecast shortfall, and simple alerts.

Data source: backend/data/production_history.csv and production_forecast.csv
(exported directly from the original M3 workbook — same numbers, same source:
IBM Monthly Statistics of Mineral Production).
"""

import csv
from pathlib import Path
from typing import List, Dict, Optional

from sqlalchemy.orm import Session
import models

DATA_DIR = Path(__file__).resolve().parent / "data"


def load_history() -> List[Dict]:
    path = DATA_DIR / "production_history.csv"
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "month": r["Month"],
                "production_tonnes": float(r["Production (tonnes)"]),
                "state": r["State"],
                "source": r["Source"],
                "data_quality": r["Data Quality"],
            })
    return rows


def load_forecast() -> List[Dict]:

    path = DATA_DIR / "production_forecast.csv"

    rows = []

    with open(path, newline="", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        for r in reader:

            forecast_value = r.get(
                "Forecast (tonnes)",
                ""
            )

            # Skip rows with missing forecast values
            if not forecast_value or not forecast_value.strip():

                continue

            try:

                forecast_tonnes = float(
                    forecast_value
                    .replace(",", "")
                    .strip()
                )

            except ValueError:

                continue

            rows.append({

                "month": r.get(
                    "Month",
                    ""
                ),

                "forecast_tonnes": forecast_tonnes,

                "method": r.get(
                    "Method",
                    "Unknown"
                ),

                "basis": r.get(
                    "Forecast Basis",
                    "Not specified"
                ),

            })

    return rows


def summary() -> Dict:
    history = load_history()
    forecast = load_forecast()

    y2024 = sum(r["production_tonnes"] for r in history if r["month"].startswith("2024"))
    y2025 = sum(r["production_tonnes"] for r in history if r["month"].startswith("2025"))
    growth_pct = ((y2025 - y2024) / y2024) * 100 if y2024 else None

    peak = max(history, key=lambda r: r["production_tonnes"])
    forecast_total_2026 = sum(r["forecast_tonnes"] for r in forecast)

    return {
        "total_2024_tonnes": round(y2024, 2),
        "total_2025_tonnes": round(y2025, 2),
        "growth_2025_vs_2024_pct": round(growth_pct, 2) if growth_pct is not None else None,
        "peak_month": peak["month"],
        "peak_month_tonnes": peak["production_tonnes"],
        "forecast_2026_total_tonnes": round(forecast_total_2026, 2),
        "model": {
            "selected": "Seasonal Naive",
            "backtest_period": "2025-07 to 2025-12",
            "mae_tonnes": 21715,
            "note": "Seasonal Naive selected over Holt Linear Trend (MAE 128,591) — "
                    "more defensible given only 24 months of history.",
        },
    }


def shortfall(db: Session) -> List[Dict]:
    """Compares forecast against any approved targets entered via the API.
    Months without an approved target stay 'Target required', matching the
    original M3 workbook's flagged pending state."""
    forecast = {r["month"]: r["forecast_tonnes"] for r in load_forecast()}
    targets = {t.month: t.target_tonnes for t in db.query(models.ProductionTarget).all()}

    results = []
    for month, forecast_tonnes in forecast.items():
        target = targets.get(month)
        if target is None:
            results.append({
                "month": month,
                "forecast_tonnes": forecast_tonnes,
                "approved_target_tonnes": None,
                "shortfall_tonnes": None,
                "status": "Target required",
            })
        else:
            shortfall_tonnes = target - forecast_tonnes
            results.append({
                "month": month,
                "forecast_tonnes": forecast_tonnes,
                "approved_target_tonnes": target,
                "shortfall_tonnes": round(shortfall_tonnes, 2),
                "status": "At risk of shortfall" if shortfall_tonnes > 0 else "On track",
            })
    return results


def alerts(db: Session) -> List[Dict]:
    """Simple, explainable alert logic — expands naturally once real 2026
    actuals and operational inputs (downtime, weather) are available."""
    out = []
    history = load_history()

    # Month-on-month decline check
    for i in range(1, len(history)):
        prev, cur = history[i - 1], history[i]
        change_pct = ((cur["production_tonnes"] - prev["production_tonnes"]) / prev["production_tonnes"]) * 100
        if change_pct <= -15:
            out.append({
                "type": "Production Drop",
                "severity": "high" if change_pct <= -25 else "medium",
                "message": f"Production fell {abs(round(change_pct,1))}% in {cur['month']} vs {prev['month']}.",
            })

    # Shortfall alerts (only meaningful once targets exist)
    for row in shortfall(db):
        if row["status"] == "At risk of shortfall":
            out.append({
                "type": "Shortfall",
                "severity": "high",
                "message": f"{row['month']} forecast ({row['forecast_tonnes']:.0f}t) is "
                           f"{row['shortfall_tonnes']:.0f}t below the approved target.",
            })

    if not out:
        out.append({
            "type": "Info",
            "severity": "low",
            "message": "No production alerts at this time. Set approved monthly targets "
                       "to enable shortfall alerts.",
        })
    return out


def set_target(db: Session, month: str, target_tonnes: float) -> models.ProductionTarget:
    existing = db.query(models.ProductionTarget).filter(models.ProductionTarget.month == month).first()
    if existing:
        existing.target_tonnes = target_tonnes
        db.commit()
        db.refresh(existing)
        return existing
    target = models.ProductionTarget(month=month, target_tonnes=target_tonnes)
    db.add(target)
    db.commit()
    db.refresh(target)
    return target
