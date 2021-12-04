from fastapi import FastAPI
from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import my_engin
from .routers import post, user, auth,vote
from .config import settings

# mit alembic nicht mehr notwendig
# models.Base.metadata.create_all(bind=my_engin)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "root"}
    



