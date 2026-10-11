from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database import get_db
from src import models, schemas
from src.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Авторизация"])

@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == data.username).first():
        raise HTTPException(400, "Пользователь с таким username уже существует")
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(400, "Пользователь с таким email уже существует")

    user = models.User(
        username=data.username,
        name=data.name,                           
        email=data.email,
        hashed_password=hash_password(data.password),  
        role=data.role,                               
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.username == form.username).first()

    if not user or not verify_password(form.password, str(user.hashed_password)):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )

    token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}