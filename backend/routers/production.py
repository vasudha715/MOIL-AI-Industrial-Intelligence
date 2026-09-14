from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

import models
import schemas

from auth import get_current_user

import services_production as svc


router = APIRouter(
    prefix="/production",
    tags=["Production & Risk"]
)


# =========================================================
# AVAILABLE HISTORICAL YEARS
# =========================================================

@router.get("/years")
def get_years(
    current_user: models.User = Depends(
        get_current_user
    )
):

    return {

        "available_historical_years":
        svc.get_available_years(),

        "latest_historical_year":
        svc.get_latest_historical_year(),

        "default_forecast_year":
        svc.get_default_forecast_year(),

    }


# =========================================================
# HISTORICAL PRODUCTION
# =========================================================

@router.get("/history")
def history(

    current_user: models.User = Depends(
        get_current_user
    )

):

    return svc.load_history()


# =========================================================
# DYNAMIC FORECAST
# =========================================================

@router.get("/forecast")
def forecast(

    forecast_year: Optional[int] = None,

    current_user: models.User = Depends(
        get_current_user
    )

):

    return svc.load_forecast(
        forecast_year
    )


# =========================================================
# PRODUCTION SUMMARY
# =========================================================

@router.get("/summary")
def get_summary(

    forecast_year: Optional[int] = None,

    current_user: models.User = Depends(
        get_current_user
    )

):

    return svc.summary(
        forecast_year
    )


# =========================================================
# TARGET VS FORECAST
# =========================================================

@router.get("/shortfall")
def get_shortfall(

    forecast_year: Optional[int] = None,

    db: Session = Depends(
        get_db
    ),

    current_user: models.User = Depends(
        get_current_user
    ),

):

    return svc.shortfall(
        db,
        forecast_year
    )


# =========================================================
# SET PRODUCTION TARGET
# =========================================================

@router.post("/target")
def set_target(

    payload: schemas.TargetIn,

    db: Session = Depends(
        get_db
    ),

    current_user: models.User = Depends(
        get_current_user
    ),

):

    target = svc.set_target(

        db,

        payload.month,

        payload.target_tonnes

    )


    return {

        "month":
        target.month,

        "target_tonnes":
        target.target_tonnes,

    }


# =========================================================
# PRODUCTION ALERTS
# =========================================================

@router.get("/alerts")
def get_alerts(

    forecast_year: Optional[int] = None,

    db: Session = Depends(
        get_db
    ),

    current_user: models.User = Depends(
        get_current_user
    ),

):

    return svc.alerts(
        db,
        forecast_year
    )