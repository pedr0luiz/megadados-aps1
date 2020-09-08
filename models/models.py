from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from helpers.helpers import generate_random_id 

class TasksStatus(str, Enum):
    to_do = "to-do"
    done = "done"

class BaseTask(BaseModel):
    title: str =  Field(..., min_length=3, max_length=30, description="Título da tarefa")
    subtitle: Optional[str] = Field("", min_length=3, max_length=50)

class OutTask(BaseTask):
    status: TasksStatus = TasksStatus.to_do.value
    id: str = Field(generate_random_id(), min_length=11, max_length=11, description="Descrição da tarefa")

class InTask(BaseTask):
    pass
