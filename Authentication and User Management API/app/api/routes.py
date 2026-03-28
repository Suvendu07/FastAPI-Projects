from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.core.config import SECRET_KEY, ALGORITHIM
from app.schema.user import UserLogin, UserRespones, UserCreate
from app.schema.token import Token
from app.core.security import hash_password, verify_password, create_access_token
from app.db.fake_db import users_db

router = APIRouter()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHIM])
        username = payload.get("sub")
        if username not in users_db:
            raise HTTPException(status_code=401, detail="invalid users")
        return users_db[username]
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token")


@router.get("/")
def home_page():
    return {"message": "This is the home page"}


@router.post("/register", response_model=UserRespones)
def register(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="user already exists")

    users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password)  
    }
    return user


@router.post("/login", response_model=Token)
def user_login(user: UserLogin):
    db_user = users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token}


@router.get("/me", response_model=UserRespones)
def read_me(current_user: dict = Depends(get_current_user)):
    return current_user


@router.patch("/me")
def partial_update(email: str, current_user: dict = Depends(get_current_user)):
    current_user["email"] = email
    return {"message": "profile updated"}


@router.delete("/me")
def delete_me(current_user: dict = Depends(get_current_user)):
    users_db.pop(current_user["username"])
    return {"message": "Account deleted"}