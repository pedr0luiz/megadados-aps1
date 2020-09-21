from fastapi import FastAPI, Depends
from api.models import not_found_response_model
from api.database import get_db
from routers import tasks
 
app = FastAPI(title="APS 1", description="Gabriel Zezze e Pedro Luiz", version="0.0.1")

app.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_db)],
    responses=not_found_response_model,
)