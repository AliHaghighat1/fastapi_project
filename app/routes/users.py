from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import List, Optional

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# -----------------------
# User Schema (input for POST)
# -----------------------
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    gender: str
    email: EmailStr
    balance: float
    is_active: bool


# -----------------------
# User Schema (output)
# -----------------------
class User(UserCreate):
    id: int


# -----------------------
# Fake Database
# -----------------------
fake_users_db: List[User] = [
    User(id=1, first_name="Ali", last_name="Mohammadi", gender="male", email="ali1@example.com", balance=120.50, is_active=True),
    User(id=2, first_name="Sara", last_name="Ahmadi", gender="female", email="sara@example.com", balance=250.00, is_active=True),
    User(id=3, first_name="Reza", last_name="Karimi", gender="male", email="reza@example.com", balance=80.75, is_active=False),
    User(id=4, first_name="Neda", last_name="Hosseini", gender="female", email="neda@example.com", balance=540.10, is_active=True),
    User(id=5, first_name="Amir", last_name="Rahimi", gender="male", email="amir@example.com", balance=15.00, is_active=True),
    User(id=6, first_name="Leila", last_name="Shirazi", gender="female", email="leila@example.com", balance=999.99, is_active=True),
    User(id=7, first_name="Hossein", last_name="Fathi", gender="male", email="hossein@example.com", balance=300.30, is_active=False),
    User(id=8, first_name="Zahra", last_name="Kazemi", gender="female", email="zahra@example.com", balance=45.20, is_active=True),
    User(id=9, first_name="Mehdi", last_name="Najafi", gender="male", email="mehdi@example.com", balance=670.00, is_active=True),
    User(id=10, first_name="Elham", last_name="Ghasemi", gender="female", email="elham@example.com", balance=10.00, is_active=False),
]


# -----------------------
# GET all users (filtering)
# -----------------------
@router.get("/", response_model=List[User])
def get_users(
    gender: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None)
):
    users = fake_users_db

    if gender:
        users = [u for u in users if u.gender == gender]

    if is_active is not None:
        users = [u for u in users if u.is_active == is_active]

    return users


# -----------------------
# GET single user
# -----------------------
@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in fake_users_db:
        if user.id == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


# -----------------------
# POST create user
# -----------------------
@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate):
    # Auto ID generation
    new_id = max([u.id for u in fake_users_db], default=0) + 1

    new_user = User(
        id=new_id,
        **user.model_dump()
    )

    fake_users_db.append(new_user)

    return new_user