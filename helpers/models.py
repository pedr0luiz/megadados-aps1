from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class TasksStatus(str, Enum):
    to_do = "to-do"
    done = "done"

class TaskSubtitle(BaseModel):
    subtitle: Optional[str] = Field(None, min_length=3, max_length=50)

class BaseTask(TaskSubtitle):
    title: str =  Field(..., min_length=3, max_length=30, description="Título da tarefa")

class OutTask(BaseTask):
    status: TasksStatus = TasksStatus.to_do.value
    id: str = Field(..., min_length=11, max_length=11, description="Descrição da tarefa")

class InTask(BaseTask):
    pass

class PatchTask(TaskSubtitle):
    status: Optional[TasksStatus] = Field(None)

