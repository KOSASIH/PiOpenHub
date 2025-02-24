# userController.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List
from .models import UserModel
from .services import AuthService
from .utils import get_db, hash_password, verify_password

# Create a router for user-related endpoints
router = APIRouter()

# Pydantic model for creating a new user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Pydantic model for user response
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

# Endpoint to create a new user
@router.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before storing
    hashed_password = hash_password(user.password)
    new_user = UserModel(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Endpoint to retrieve a list of users
@router.get("/users/", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

# Endpoint to retrieve a specific user by ID
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Endpoint for user login
@router.post("/login/")
async def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token for the user
    access_token = AuthService.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
