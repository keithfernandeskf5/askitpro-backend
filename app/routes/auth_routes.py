print("AUTH ROUTES LOADED")
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from app.services.auth import hash_password
from app.database import get_db
from app.models.db_models import Teacher
from app.services.auth import (
    verify_password,
    create_access_token
)

router = APIRouter()


@router.post("/teacher/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    teacher = db.query(Teacher).filter(
        Teacher.email == form_data.username
    ).first()

    if not teacher:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    if not verify_password(
        form_data.password,
        teacher.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(
        data={"sub": teacher.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
@router.post("/create-teacher")
def create_teacher(db: Session = Depends(get_db)):

    teacher = Teacher(
        email="teacher@test.com",
        hashed_password=hash_password("1234")
    )

    db.add(teacher)
    db.commit()

    return {"message": "Teacher created"}