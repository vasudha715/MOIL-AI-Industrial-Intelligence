from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/mines", tags=["Mine Management"])


@router.post("/", response_model=schemas.MineOut)
def create_mine(
    payload: schemas.MineCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    mine = models.Mine(
        name=payload.name,
        location_name=payload.location_name,
        latitude=payload.latitude,
        longitude=payload.longitude,
        owner_id=current_user.id,
    )
    db.add(mine)
    db.commit()
    db.refresh(mine)
    return mine


@router.get("/", response_model=List[schemas.MineOut])
def list_mines(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.Mine).filter(models.Mine.owner_id == current_user.id).all()


@router.get("/{mine_id}", response_model=schemas.MineOut)
def get_mine(
    mine_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    mine = db.query(models.Mine).filter(
        models.Mine.id == mine_id, models.Mine.owner_id == current_user.id
    ).first()
    if not mine:
        raise HTTPException(status_code=404, detail="Mine not found")
    return mine


@router.delete("/{mine_id}")
def delete_mine(
    mine_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    mine = db.query(models.Mine).filter(
        models.Mine.id == mine_id, models.Mine.owner_id == current_user.id
    ).first()
    if not mine:
        raise HTTPException(status_code=404, detail="Mine not found")
    db.delete(mine)
    db.commit()
    return {"status": "deleted"}
