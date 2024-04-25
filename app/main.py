from fastapi import FastAPI

from app.auth import routes as auth_routes
from app.tasks import routes as tasks_routes
from app.dependecies import get_current_user
app = FastAPI()
app.include_router(auth_routes.router)
app.include_router(tasks_routes.router, dependecies=[get_current_user])