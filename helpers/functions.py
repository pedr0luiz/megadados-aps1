import secrets
from typing import List
from helpers.models import TasksStatus, OutTask

def generate_random_id() -> str:
    return secrets.token_urlsafe(8)

def filter_tasks(global_tasks: List[OutTask], status: TasksStatus) -> List[OutTask]:
    response = []
    for task in global_tasks:
        if task.status == status:
            response.append(task)
    return response

def find_task_by_id(global_tasks: List[OutTask], id: str) -> (OutTask, int) or None:
    for index in range(len(global_tasks)):
        if global_tasks[index].id == id:
            return global_tasks[index], index
    return None, None