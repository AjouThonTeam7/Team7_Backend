from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from . import emptytime_crud, emptytime_schema
from database import get_db

router = APIRouter()


@router.post("/users/{user_id}/empty_times/")
def create_user_empty_time(user_id: int, weekday: str, periods: list, db: Session = Depends(get_db)):
    return crud.create_empty_time(db=db, user_id=user_id, weekday=weekday, periods=periods)


@router.get("/users/{user_id}/empty_times/")
def read_user_empty_times(user_id: int, db: Session = Depends(get_db)):
    db_empty_times = crud.get_empty_times(db, user_id=user_id)
    if db_empty_times is None:
        raise HTTPException(status_code=404, detail="Empty times not found")
    return db_empty_times


@router.post("/find_overlap_users/")
def find_overlap_users(request: emptytime_schema.RequestSchema, db: Session = Depends(get_db)):
    overlap_users_by_period = get_overlap_users_by_period(
        db, user_id=request.id, weekday=request.weekday)
    return overlap_users_by_period
