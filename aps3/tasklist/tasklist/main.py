# pylint: disable=missing-module-docstring
from fastapi import FastAPI

from .routers import task, user
from utils import utils

tags_metadata = [
    {
        'name': 'task',
        'description': 'Operations related to tasks.',
    },
]

app = FastAPI(
    title='Task list',
    description='Task-list project for the **Megadados** course',
    openapi_tags=tags_metadata,
)

app.dependency_overrides[utils.get_config_filename] = utils.get_config_test_filename

# Task routes
app.include_router(task.router, prefix='/task', tags=['task'])

# User Routes
app.include_router(user.router, prefix='/user', tags=['user'])
