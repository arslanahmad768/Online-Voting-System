from fastapi import FastAPI
from . import routes

app = FastAPI()

@app.get("/")
async def root():
    return "Welcome to Online Voting System"

app.include_router(routes.router,tags=['Main App'])