from fastapi import FastAPI, Query, HTTPException, Body, Depends
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
import secrets
from helpers.models import OutTask, InTask, TasksStatus, PatchTask, NotFoundResponse
from helpers.functions import generate_random_id, filter_tasks, find_task_by_id
 
app = FastAPI(title="APS 1", description="Gabriel Zezze e Pedro Luiz", version="0.0.1")

class DBSession:
    tasks: List[OutTask] = []
    def __init__(self):
        self.tasks = DBSession.tasks
def get_db():
    return DBSession()

not_found_response_model = {
    404: {
        "description": "Tarefa não encontrada",
        "model": NotFoundResponse
    }
}

@app.post(
    "/tasks",
    response_model = OutTask,
    status_code =  201,
    summary = "Rota para criar tasks",
    description = "Esta rota é usada para criar as tasks.",
    response_description = "A task é inserida no banco de dados e retornada para o usúario com seu id."
)
async def create_task(task: InTask, db: DBSession = Depends(get_db)):
    existing_task = True
    new_task_id = generate_random_id()
    while existing_task:
        existing_task, _idx = find_task_by_id(db.tasks, new_task_id)
        if existing_task:
            new_task_id = generate_random_id()
    out_task = OutTask(**task.dict(), id=new_task_id)
    db.tasks.append(out_task)
    return out_task

@app.get(
    "/tasks",
    response_model = List[OutTask],
    responses = not_found_response_model,
    summary = "Rota para buscar tasks",
    description = "Esta rota é usada para buscar tasks no banco de dados, sendo possivel a busca de uma task especifica, todas as tasks ou filtragem por status.",
    response_description = "A(s) task(s) é(são) devolvida(s) para o usúario em uma lista."
)
async def get_tasks(status: Optional[TasksStatus] = None, 
                    task_id: Optional[str] = Query(None, min_length=11, max_length=11), 
                    db: DBSession = Depends(get_db)):
    if task_id:
        filtered_task, _idx = find_task_by_id(db.tasks, task_id)
        if filtered_task:
            return [filtered_task]
        raise HTTPException(status_code=404, detail=f"Tarefa {task_id} não encontrada")

    filtered_tasks = filter_tasks(db.tasks, status) if status else db.tasks
    return filtered_tasks

@app.delete(
    "/tasks/{task_id}",
    response_model = OutTask,
    status_code = 202,
    responses=not_found_response_model,
    summary = "Rota para deletar tasks",
    description = "Esta rota é usada para deletar tasks presentes no banco de dados",
    response_description = "A task deletada é removida do banco de dados e devolvida uma copia para o usúario."
)
async def delete_task(task_id: str = Query(..., min_length=11, max_length=11), db: DBSession = Depends(get_db)):
    task, _index = find_task_by_id(db.tasks, task_id)
    if task:
        db.tasks.remove(task)
        return task
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.patch(
    "/tasks/{task_id}",
    response_model = OutTask,
    responses=not_found_response_model,
    summary = "Rota para alterar tasks",
    description = "Esta rota é usada para alterar uma task especifica.",
    response_description = "A task já alterada é devolvida para o usúario."
)
async def patch_task(
    task_id: str = Query(..., min_length=11, max_length=11), 
    partial_task: PatchTask = Body(...), 
    db: DBSession = Depends(get_db)):
    
    task, index = find_task_by_id(db.tasks, task_id)
    if task:
        update_data = partial_task.dict(exclude_unset=True)
        updated_item = task.copy(update=update_data)
        db.tasks[index] = updated_item
        return updated_item
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")