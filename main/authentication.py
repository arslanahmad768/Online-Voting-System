from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime,timedelta
from typing import Union
from jose import JWTError, jwt
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "d0b62ece75aab9576c0812eff58aac1b1ef5739e47f946633ea0ea555f99bea5"
ALGORITHM = "HS256"

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, password=fake_hashed_password,first_name=user.first_name,last_name=user.last_name,username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_password_hash(password):
    return pwd_context.hash(password)

class UserInDB(schemas.User):
    password: str


def get_user(db, email: str):
    print ("in Get User function")
    print("enter i ")
    user_dict =  db.query(models.User).filter(models.User.email == email).first()
    if user_dict:
        print("enter in Loop")
    # user_dict = db[email]
        return user_dict

def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


def authenticate_user(db:Session, email: str, password: str): 
    user = get_user(db, email)
    print("return data is ",user)
    # breakpoint()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
