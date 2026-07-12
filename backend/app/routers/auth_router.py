from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.schemas.user_schema import UserRegister, UserLogin
from app.services.auth_service import hash_password, verify_password
from app.database import SessionLocal
from app.services.jwt_service import create_access_token
from fastapi import Depends
from app.services.auth_dependency import get_current_user



router = APIRouter(tags=["Authentication"])


# ==========================
# REGISTER USER
# ==========================
@router.post("/register")
def register_user(user: UserRegister):

    db = SessionLocal()

    existing_user = db.execute(
        text("SELECT * FROM users WHERE email = :email"),
        {"email": user.email}
    ).fetchone()

    if existing_user:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    db.execute(
        text("""
            INSERT INTO users (name, email, password_hash)
            VALUES (:name, :email, :password_hash)
        """),
        {
            "name": user.name,
            "email": user.email,
            "password_hash": hashed_password
        }
    )

    db.commit()
    db.close()

    return {
        "message": "User registered successfully"
    }


# ==========================
# LOGIN USER
# ==========================
@router.post("/login")
def login_user(user: UserLogin):

    db = SessionLocal()

    existing_user = db.execute(
        text("""
            SELECT email, password_hash
            FROM users
            WHERE email = :email
        """),
        {
            "email": user.email
        }
    ).fetchone()

    db.close()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    access_token = create_access_token(data={"sub": existing_user.email})

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }
@router.get("/me")
def get_me(current_user=Depends(get_current_user)):

    return {
        "email": current_user["sub"]
    }