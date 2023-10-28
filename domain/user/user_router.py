from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import user_crud, user_schema
from database import get_db
from typing import List
from ..crowler.main import run_crowler
from ..emptytime.emptytime_crud import create_empty_time


router = APIRouter()


@router.post("/register", response_model=user_schema.UserSchema)
def create_user(user: user_schema.UserSchema, db: Session = Depends(get_db)):
    data = run_crowler(user.user_id, user.user_pw)
    name = data["name"]
    major = data["major"]
    subject = data["subject"]
    day = data["day"]
    user.major = major
    user.name = name
    user.subjects = subject
    for d in day.items():
        create_empty_time(db, user_id=user.user_id, weekday=d[0], periods=d[1])
    db_user = user_crud.get_user(db, user_id=user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return user_crud.create_user(db, user=user)


@router.post("/login", response_model=user_schema.UserSchema)
def login_user(user: user_schema.CreateUser, db: Session = Depends(get_db)):
    db_user = user_crud.authenticate_user(
        db, user_id=user.user_id, user_pw=user.user_pw
    )
    if db_user is None:
        raise HTTPException(status_code=400, detail="Incorrect user ID or password")
    return db_user


@router.delete("/delete/{user_id}", response_model=user_schema.UserSchema)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = user_crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/get/{user_id}", response_model=user_schema.UserSchema)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/overlapping-users/")
async def get_overlapping_users(user_id: int, day: str, db: Session = Depends(get_db)):
    overlapping_users = user_crud.get_overlapping_users(db, user_id=user_id, day=day)
    if overlapping_users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return overlapping_users
