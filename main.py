from fastapi import FastAPI, Query, HTTPException, Body
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
import secrets
from helpers.models import OutTask, InTask, TasksStatus, PatchTask
from helpers.functions import generate_random_id, filter_tasks, find_task_by_id
 
app = FastAPI(title="APS 1", description="Gabriel Zezze e Pedro Luiz", version="0.0.1")

global_tasks: List[OutTask] = []

@app.post("/tasks", response_model = OutTask, status_code=201)
async def create_task(task: InTask):
    out_task = OutTask(**task.dict(), id=generate_random_id())
    global_tasks.append(out_task)
    return out_task

@app.get("/tasks", response_model = List[OutTask])
async def get_tasks(status: Optional[TasksStatus] = None):
    filtered_tasks = filter_tasks(global_tasks, status) if status else global_tasks
    return filtered_tasks

@app.delete("/tasks/{task_id}", response_model = OutTask, status_code = 202)
async def delete_task(task_id: str = Query(..., min_length=11, max_length=11)):
    task, _index = find_task_by_id(global_tasks, task_id)
    if task:
        global_tasks.remove(task)
        return task
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.patch("/tasks/{task_id}")
async def patch_task(
    task_id: str = Query(..., min_length=11, max_length=11), 
    partial_task: PatchTask = Body(...)):
    task, index = find_task_by_id(global_tasks, task_id)
    if task:
        update_data = partial_task.dict(exclude_unset=True)
        updated_item = task.copy(update=update_data)
        global_tasks[index] = updated_item
        return updated_item
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")