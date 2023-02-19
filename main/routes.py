from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.requests import Request
from . import schemas,database,authentication
from datetime import datetime, timedelta

router = APIRouter()

templates = Jinja2Templates(directory="templates")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#------ Funcions ------

@router.post("/registration/")
async def registration(user:schemas.UserCreate,db:Session = Depends(database.get_db)):
    print("request Data is ",user)
    db_user = authentication.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return authentication.create_user(db=db,user=user)

@router.post("/login/")
async def login_for_access_token(user:schemas.login,db:Session = Depends(database.get_db)):
    user = authentication.authenticate_user(db, user.email, user.password)
    print("user is ",user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    # return {"access_token": access_token, "token_type": "bearer"}
    return {"access_token": access_token}

# @router.get("/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# @router.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]


# -- HTML Pages ---

@router.get('/loginpage/',response_class=HTMLResponse)
async def loginPage(request:Request):
    return templates.TemplateResponse("login.html",{"request":request,"title":"Login"})
    
@router.get('/registrationpage/',response_class=HTMLResponse)
async def loginPage(request:Request):
    return templates.TemplateResponse("registration.html",{"request":request,"title":"Sign UP"})

@router.get('/Homepage/',response_class=HTMLResponse)
async def loginPage(request:Request):
    return templates.TemplateResponse("index.html",{"request":request,"title":"Home"})