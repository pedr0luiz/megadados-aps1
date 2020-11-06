# pylint: disable=missing-module-docstring,missing-class-docstring
from typing import Optional
import uuid

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

# pylint: disable=too-few-public-methods
class User(BaseModel):
    username: str = Field(
        'Identificador do usúario para login',
        title='Identificador do usúario',
        max_length=45
    )

    first_name: str = Field(
        'Primeiro Nome do usúario',
        title='Primeiro nome',
        max_length=45
    )

    last_name: str = Field(
        'Ultimo nome do usúario',
        title='Sobrenome',
        max_length=45
    )

    class Config:
        schema_extra = {
            'example': {
                'username': 'pedrao_51',
                'first_name': 'Pedro',
                'last_name': 'Luiz'
            }
        }


# pylint: disable=too-few-public-methods
class Task(BaseModel):
    description: Optional[str] = Field(
        'no description',
        title='Task description',
        max_length=1024,
    )
    completed: Optional[bool] = Field(
        False,
        title='Shows whether the task was completed',
    )
    user_id: uuid.UUID = Field(
        'Identificador do usúario',
        title='Identificador do usúario'
    )

    class Config:
        schema_extra = {
            'example': {
                'description': 'Buy baby diapers',
                'completed': False,
                'user_id': 'id_usuario_x'
            }
        }
