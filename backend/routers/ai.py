import sys
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
import models
from auth import get_current_user
import services_production as svc
import ai_engine

M2_DIR = Path(__file__).resolve().parent.parent / "m2_exploration"
if str(M2_DIR) not in sys.path:
    sys.path.append(str(M2_DIR))

from engine.industrial_analysis_engine import analyze_industrial_area  # noqa: E402

router = APIRouter(prefix="/ai", tags=["AI Recommendations"])


class RecommendationRequest(BaseModel):
    location: Optional[str] = None  # if given, runs a fresh exploration analysis
    buffer_degrees: float = 0.01
    grid_rows: int = 10
    grid_cols: int = 10


@router.post("/recommendations")
def get_recommendations(
    payload: RecommendationRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    exploration_result = None
    if payload.location:
        try:
            raw = analyze_industrial_area(
                location_name=payload.location,
                buffer_degrees=payload.buffer_degrees,
                grid_rows=payload.grid_rows,
                grid_cols=payload.grid_cols,
            )
            exploration_result = {
                "location": raw["location"],
                "weather_risk": raw["weather_risk"],
                "satellite": raw["satellite"],
                "top_zones": raw["top_zones"].to_dict(orient="records"),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Exploration engine error: {e}")

    production_summary = svc.summary()
    shortfall_rows = svc.shortfall(db)

    recommendations = ai_engine.generate_recommendations(
        exploration_result=exploration_result,
        production_summary=production_summary,
        shortfall_rows=shortfall_rows,
    )

    return {
        "status": "success",
        "location_analyzed": payload.location,
        "recommendations": recommendations,
    }
