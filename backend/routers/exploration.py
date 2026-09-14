"""
Exploration & GIS router.

This router exposes the M2 industrial exploration engine
through the unified MOIL AI backend.
"""

import json
import sys
import math
from pathlib import Path

import numpy as np

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from auth import get_current_user


# ====================================================
# MAKE M2 ENGINE IMPORTABLE
# ====================================================

M2_DIR = Path(__file__).resolve().parent.parent / "m2_exploration"

if str(M2_DIR) not in sys.path:
    sys.path.append(str(M2_DIR))


from engine.industrial_analysis_engine import analyze_industrial_area


# ====================================================
# ROUTER
# ====================================================

router = APIRouter(
    prefix="/exploration",
    tags=["Exploration & GIS"]
)


# ====================================================
# CLEAN DATA FOR JSON
# ====================================================

def clean_for_json(value):

    if isinstance(value, dict):

        return {
            key: clean_for_json(val)
            for key, val in value.items()
        }


    if isinstance(value, list):

        return [
            clean_for_json(item)
            for item in value
        ]


    if isinstance(value, np.generic):

        value = value.item()


    if isinstance(value, float):

        if math.isnan(value) or math.isinf(value):

            return None


    return value


# ====================================================
# ANALYZE AREA
# ====================================================

@router.post("/analyze")
def analyze(

    request: schemas.AnalysisRequest,

    db: Session = Depends(get_db),

    current_user: models.User = Depends(
        get_current_user
    ),

):

    try:

        result = analyze_industrial_area(

            location_name=request.location,

            buffer_degrees=request.buffer_degrees,

            grid_rows=request.grid_rows,

            grid_cols=request.grid_cols,

        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=f"Exploration engine error: {e}"

        )


    # ====================================================
    # CONVERT DATAFRAME RESULTS
    # ====================================================

    top_zones = result[
        "top_zones"
    ].to_dict(
        orient="records"
    )


    exploration_zones = result[
        "exploration_grid"
    ].to_dict(
        orient="records"
    )


    # ====================================================
    # CLEAN NaN / INF VALUES
    # ====================================================

    top_zones = clean_for_json(
        top_zones
    )


    exploration_zones = clean_for_json(
        exploration_zones
    )


    # ====================================================
    # RESPONSE
    # ====================================================

    response = {

        "status":

            "success",


        "location":

            clean_for_json(
                result["location"]
            ),


        "weather_risk":

            clean_for_json(
                result["weather_risk"]
            ),


        "satellite":

            clean_for_json(
                result["satellite"]
            ),


        "total_zones":

            clean_for_json(
                result["total_zones"]
            ),


        "priority_summary":

            clean_for_json(
                result["priority_summary"]
            ),


        "top_zones":

            top_zones,


        "exploration_zones":

            exploration_zones,

    }


    # ====================================================
    # OPTIONAL: SAVE ANALYSIS FOR A MINE
    # ====================================================

    if request.mine_id is not None:

        mine = (

            db.query(
                models.Mine
            )

            .filter(

                models.Mine.id
                ==
                request.mine_id,

                models.Mine.owner_id
                ==
                current_user.id,

            )

            .first()

        )


        if not mine:

            raise HTTPException(

                status_code=404,

                detail="Mine not found for this user"

            )


        record = models.ExplorationResult(

            mine_id=mine.id,


            location=json.dumps(
                response["location"]
            ),


            weather_risk=json.dumps(
                response["weather_risk"]
            ),


            satellite=json.dumps(
                response["satellite"]
            ),


            total_zones=response[
                "total_zones"
            ],


            priority_summary=json.dumps(
                response["priority_summary"]
            ),


            top_zones=json.dumps(
                top_zones
            ),

        )


        db.add(
            record
        )


        db.commit()


    # ====================================================
    # ALWAYS RETURN RESPONSE
    # ====================================================

    return response


# ====================================================
# EXPLORATION HISTORY
# ====================================================

@router.get("/history/{mine_id}")
def exploration_history(

    mine_id: int,

    db: Session = Depends(get_db),

    current_user: models.User = Depends(
        get_current_user
    ),

):

    mine = (

        db.query(
            models.Mine
        )

        .filter(

            models.Mine.id
            ==
            mine_id,


            models.Mine.owner_id
            ==
            current_user.id,

        )

        .first()

    )


    if not mine:

        raise HTTPException(

            status_code=404,

            detail="Mine not found"

        )


    records = (

        db.query(
            models.ExplorationResult
        )

        .filter(

            models.ExplorationResult.mine_id
            ==
            mine_id

        )

        .order_by(

            models.ExplorationResult.created_at.desc()

        )

        .all()

    )


    return [

        {

            "id":

                r.id,


            "location":

                json.loads(
                    r.location
                )
                if r.location
                else None,


            "weather_risk":

                json.loads(
                    r.weather_risk
                )
                if r.weather_risk
                else None,


            "satellite":

                json.loads(
                    r.satellite
                )
                if r.satellite
                else None,


            "total_zones":

                r.total_zones,


            "priority_summary":

                json.loads(
                    r.priority_summary
                )
                if r.priority_summary
                else None,


            "top_zones":

                json.loads(
                    r.top_zones
                )
                if r.top_zones
                else None,


            "created_at":

                r.created_at.isoformat(),

        }

        for r in records

    ]