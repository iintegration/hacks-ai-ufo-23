from fastapi import FastAPI, APIRouter, Depends

from app.dependencies import verify_token
from app.routers import subjects, auth, search, tasks

app = FastAPI()
app.include_router(auth.router)

private_router = APIRouter(dependencies=[Depends(verify_token)])
private_router.include_router(search.router)
private_router.include_router(tasks.router)
private_router.include_router(subjects.router)

app.include_router(private_router)
