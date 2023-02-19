from fastapi import FastAPI
from . import routes,database,models
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "Welcome to Online Voting System"

app.include_router(routes.router,tags=['Main App'])