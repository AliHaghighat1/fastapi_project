from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# -----------------------
# GET all users (with filters)
# -----------------------
@router.get("/", response_model=List[UserResponse])
def get_users(
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(UserModel)

    # -----------------------
    # Exact matches
    # -----------------------
    if gender:
        query = query.filter(UserModel.gender == gender)

    if is_active is not None:
        query = query.filter(UserModel.is_active == is_active)

    # -----------------------
    # Partial / flexible search
    # -----------------------
    if first_name:
        query = query.filter(UserModel.first_name.ilike(f"%{first_name}%"))

    if last_name:
        query = query.filter(UserModel.last_name.ilike(f"%{last_name}%"))

    if email:
        query = query.filter(UserModel.email.ilike(f"%{email}%"))

    return query.all()


# -----------------------
# GET single user
# -----------------------
@router.get("/{public_id}", response_model=UserResponse)
def get_user(public_id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.public_id == public_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# -----------------------
# CREATE user
# -----------------------
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # check duplicate email
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = UserModel(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -----------------------
# UPDATE user (PUT)
# -----------------------
@router.put("/{public_id}", response_model=UserResponse)
def update_user(public_id: str, user_update: UserCreate, db: Session = Depends(get_db)):

    user = db.query(UserModel).filter(UserModel.public_id == public_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # check email duplication (exclude current user)
    email_exists = db.query(UserModel).filter(
        UserModel.email == user_update.email,
        UserModel.public_id != public_id
    ).first()

    if email_exists:
        raise HTTPException(status_code=400, detail="Email already exists")

    # update fields
    for key, value in user_update.model_dump().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


# -----------------------
# DELETE user
# -----------------------
@router.delete("/{public_id}")
def delete_user(public_id: str, db: Session = Depends(get_db)):

    user = db.query(UserModel).filter(UserModel.public_id == public_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}