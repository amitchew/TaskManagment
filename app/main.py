from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.tasks.routes import router as tasks_router
from app.database.base import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(tasks_router, prefix="/tasks")
