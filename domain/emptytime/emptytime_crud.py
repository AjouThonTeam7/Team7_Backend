from sqlalchemy.orm import Session
import models
from . import emptytime_router, emptytime_schema
from typing import Dict, List
from ..user.user_schema import UserSchema


def create_empty_time(db: Session, user_id: int, weekday: str, periods: list):
    db_empty_time = models.EmptyTime(
        user_id=user_id, weekday=weekday, periods=periods)
    db.add(db_empty_time)
    db.commit()
    db.refresh(db_empty_time)
    return db_empty_time


def get_empty_times(db: Session, user_id: int):
    return db.query(models.EmptyTime).filter(models.EmptyTime.user_id == user_id).all()


def get_overlap_users_by_period(db: Session, user_id: int, weekday: str) -> Dict[str, List[UserSchema]]:
    user_empty_time = db.query(models.EmptyTime).filter(
        models.EmptyTime.user_id == user_id,
        models.EmptyTime.weekday == weekday
    ).first()

    if not user_empty_time:
        return {}

    response_data = {}
    for period in user_empty_time.periods:
        matching_empty_times = db.query(models.EmptyTime).filter(
            models.EmptyTime.weekday == weekday,
            # Assumes periods is a JSON array
            models.EmptyTime.periods.contains([period])
        ).all()

        user_ids = [empty_time.user_id for empty_time in matching_empty_times]
        overlap_users = db.query(models.User).filter(
            models.User.id.in_(user_ids)).all()
        response_data[period] = [UserSchema.from_orm(
            user) for user in overlap_users]

    return response_data
