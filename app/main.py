from fastapi import APIRouter, Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.dependencies import verify_token
from app.routers import auth, search, subjects, tasks, upload


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

private_router = APIRouter(dependencies=[Depends(verify_token)])
private_router.include_router(search.router)
private_router.include_router(tasks.router)
private_router.include_router(subjects.router)
private_router.include_router(upload.router)

app.include_router(private_router)
