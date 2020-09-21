from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class TasksStatus(str, Enum):
    to_do = "to-do"
    done = "done"

class TaskSubtitle(BaseModel):
    subtitle: Optional[str] = Field(None, min_length=3, max_length=50, description="Subtitulo da tarefa", example="Uma tarefa não tão simples")

class BaseTask(TaskSubtitle):
    title: str =  Field(..., min_length=3, max_length=30, description="Título da tarefa", example="Megatask")

class OutTask(BaseTask):
    status: TasksStatus = TasksStatus.to_do.value
    id: str = Field(..., min_length=11, max_length=11, description="Identificador da tarefa", example="<Id gerado automaticamente>")

class InTask(BaseTask):
    pass

class PatchTask(TaskSubtitle):
    status: Optional[TasksStatus] = Field(None, description="Status da tarefa")

class NotFoundResponse(BaseModel):
    detail: str = Field(..., description="Motivo de falha na requisição", example="Tarefa <id da tarefa pesquisada> não encontrada")

not_found_response_model = {
    404: {
        "description": "Tarefa não encontrada",
        "model": NotFoundResponse
    }
}