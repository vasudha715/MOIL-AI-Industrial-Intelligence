"""
Unified AI Recommendation Engine (M4).

Combines:
- M2 Exploration Intelligence
- Weather Risk
- M3 Production Intelligence
- Production Shortfall Risk

Generates clear, prioritized recommendations for industrial users.
"""

from typing import Dict, List, Optional


def get_location_name(location) -> str:
    """
    Convert the M2 location object into a clean location name.
    """

    if not location:
        return "the analyzed area"

    if isinstance(location, str):
        return location

    if isinstance(location, dict):
        return (
            location.get("name")
            or location.get("location")
            or location.get("display_name")
            or "the analyzed area"
        )

    return str(location)


def get_weather_status(weather_risk) -> Optional[str]:
    """
    Extract weather risk status safely from the M2 result.
    """

    if not weather_risk:
        return None

    if isinstance(weather_risk, str):
        return weather_risk.lower()

    if isinstance(weather_risk, dict):

        status = (
            weather_risk.get("risk_level")
            or weather_risk.get("level")
            or weather_risk.get("status")
            or weather_risk.get("risk")
            or weather_risk.get("weather_risk")
            or weather_risk.get("weather_status")
        )

        if status:
            return str(status).lower()

    return None


def get_weather_note(weather_status) -> str:
    """
    Convert weather status into an industrial recommendation.
    """

    if not weather_status:
        return (
            "Weather information was not available "
            "for this analysis."
        )

    if weather_status in (
        "low",
        "clear",
        "favorable",
        "good",
    ):
        return (
            "Current weather conditions are suitable "
            "for field exploration activities."
        )

    if weather_status in (
        "medium",
        "moderate",
    ):
        return (
            "Moderate weather risk detected. "
            "Field operations should be monitored."
        )

    if weather_status in (
        "high",
        "severe",
        "poor",
    ):
        return (
            "Weather risk is elevated. "
            "Consider delaying field exploration activities."
        )

    return (
        f"Current weather risk level: "
        f"{weather_status.upper()}."
    )


def generate_recommendations(
    exploration_result: Optional[Dict] = None,
    production_summary: Optional[Dict] = None,
    shortfall_rows: Optional[List[Dict]] = None,
) -> List[Dict]:

    recommendations = []

    # ==========================================
    # EXPLORATION RECOMMENDATIONS
    # ==========================================

    if exploration_result:

        top_zones = (
            exploration_result.get("top_zones")
            or []
        )

        location_name = get_location_name(
            exploration_result.get("location")
        )

        weather_status = get_weather_status(
            exploration_result.get("weather_risk")
        )

        weather_note = get_weather_note(
            weather_status
        )

        for index, zone in enumerate(
            top_zones[:3],
            start=1,
        ):

            score = zone.get(
                "PROSPECTIVITY_SCORE"
            )

            if score is None:

                score = zone.get(
                    "prospectivity_score"
                )

            if score is None:

                score = 0

            priority = (
                "high"
                if float(score) >= 70
                else "medium"
            )

            recommendations.append({

                "category": "Exploration",

                "priority": priority,

                "title": (
                    f"Validate Priority "
                    f"Exploration Zone {index}"
                ),

                "reason": (
                    f"Zone {index} in "
                    f"{location_name} has a "
                    f"prospectivity score of "
                    f"{float(score):.2f}."
                ),

                "weather_note": weather_note,

                "recommended_next_step": (
                    "Conduct geological field validation "
                    "and detailed mineral sampling before "
                    "planning drilling operations."
                ),

            })

        if not top_zones:

            recommendations.append({

                "category": "Exploration",

                "priority": "low",

                "title": (
                    "No high-priority exploration "
                    "zones identified"
                ),

                "reason": (
                    "The current analysis did not "
                    "identify priority exploration zones."
                ),

                "recommended_next_step": (
                    "Consider expanding the search "
                    "area or buffer radius."
                ),

            })

    # ==========================================
    # PRODUCTION RECOMMENDATIONS
    # ==========================================

    if production_summary:

        growth = production_summary.get(
            "growth_2025_vs_2024_pct"
        )

        if growth is not None:

            if growth < 0:

                recommendations.append({

                    "category": "Production",

                    "priority": "high",

                    "title": (
                        "Year-over-year production "
                        "decline detected"
                    ),

                    "reason": (
                        f"2025 production decreased by "
                        f"{abs(growth)}% compared "
                        f"with 2024."
                    ),

                    "recommended_next_step": (
                        "Review production operations, "
                        "equipment performance and "
                        "operational constraints."
                    ),

                })

            elif growth > 15:

                recommendations.append({

                    "category": "Production",

                    "priority": "low",

                    "title": (
                        "Strong year-over-year "
                        "production growth"
                    ),

                    "reason": (
                        f"2025 production increased by "
                        f"{growth}% compared with 2024."
                    ),

                    "recommended_next_step": (
                        "Validate whether the 2026 "
                        "production forecast can sustain "
                        "this growth trend."
                    ),

                })

    # ==========================================
    # SHORTFALL RECOMMENDATIONS
    # ==========================================

    if shortfall_rows:

        at_risk = [

            row

            for row in shortfall_rows

            if row.get("status")
            == "At risk of shortfall"

        ]

        pending = [

            row

            for row in shortfall_rows

            if row.get("status")
            == "Target required"

        ]

        for row in at_risk:

            recommendations.append({

                "category": "Risk",

                "priority": "high",

                "title": (
                    f"Production shortfall risk: "
                    f"{row['month']}"
                ),

                "reason": (
                    f"Forecast production is "
                    f"{row['forecast_tonnes']:.0f} tonnes. "
                    f"This is "
                    f"{row['shortfall_tonnes']:.0f} tonnes "
                    f"below the approved target of "
                    f"{row['approved_target_tonnes']:.0f} tonnes."
                ),

                "recommended_next_step": (
                    "Review production capacity and "
                    "operational constraints. Consider "
                    "corrective actions to reduce the "
                    "forecast gap."
                ),

            })

        if pending and not at_risk:

            recommendations.append({

                "category": "Risk",

                "priority": "medium",

                "title": (
                    "Production targets require approval"
                ),

                "reason": (
                    f"{len(pending)} month(s) do not "
                    "have approved production targets."
                ),

                "recommended_next_step": (
                    "Enter approved monthly production "
                    "targets to enable shortfall analysis."
                ),

            })

    # ==========================================
    # DEFAULT RECOMMENDATION
    # ==========================================

    if not recommendations:

        recommendations.append({

            "category": "General",

            "priority": "low",

            "title": (
                "No recommendations yet"
            ),

            "reason": (
                "Run exploration analysis or "
                "configure production targets."
            ),

            "recommended_next_step": (
                "Use the Exploration GIS and "
                "Production Intelligence modules."
            ),

        })

    # ==========================================
    # SORT BY PRIORITY
    # ==========================================

    priority_order = {

        "high": 0,

        "medium": 1,

        "low": 2,

    }

    recommendations.sort(

        key=lambda item: priority_order.get(
            item.get("priority"),
            3,
        )

    )

    return recommendations