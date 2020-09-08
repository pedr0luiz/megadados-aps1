from fastapi import FastAPI, Query, HTTPException
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
import secrets
from models.models import OutTask, InTask, TasksStatus
from helpers.helpers import generate_random_id, filter_tasks, find_task
 
app = FastAPI(title="APS 1", description="Gabriel Zezze e Pedro Luiz", version="0.0.1")

global_tasks = []

@app.post("/tasks", response_model = OutTask, status_code=201)
async def create_task(task: InTask):
    out_task = OutTask(**task.dict(), id=generate_random_id())
    global_tasks.append(out_task.dict())
    return out_task

@app.get("/tasks", response_model = List[OutTask])
async def get_tasks(status: Optional[TasksStatus] = None):
    filtered_tasks = filter_tasks(global_tasks, status) if status else global_tasks
    return filtered_tasks

@app.delete("/tasks", response_model = OutTask, status_code = 202)
async def delete_task(id: str = Query(..., min_length=11, max_length=11)):
    task = find_task(global_tasks, id)
    global_tasks.remove(task)
    if task:
        return task
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

# class Item(BaseModel):
#     name: ModelName
#     description: Optional[str] = Field(None, min_length=3, description="testandooo")
#     price: float
#     tax: Optional[float] = None

# class User(BaseModel):
#     name: str
#     full_name: Optional[str] = None

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, teste: Optional[str] = Query(None, max_length=50, min_length=30)):
#     return {"item_id": item_id}

# @app.get("/model/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name == ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}

# @app.post("/item/", response_model = Item)
# async def create_item(item: Item, user: Optional[User] = None):
#     return item