from ..models import User
from ..database import DBSession, get_db

from fastapi import APIRouter, HTTPException, Depends
import uuid
from typing import Dict

router = APIRouter()

@router.post(
    '',
    summary='Creates a new user',
    description='Creates a new user and returns its UUID.',
    response_model=uuid.UUID,
)
async def create_user(new_user: User, db: DBSession = Depends(get_db)):
    return db.create_user(new_user)


@router.get(
    '/{uuid_}',
    summary='Reads a user',
    description='Fetch user info.',
    response_model=User,
)
async def fetch_user(uuid_: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        return db.fetch_user(uuid_)
    except KeyError as e:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        ) from e

@router.put(
    '/{uuid_}',
    summary='Replaces an user',
    description='Replaces an user identified by its UUID.',
)
async def replace_user(
        uuid_: uuid.UUID,
        item: User,
        db: DBSession = Depends(get_db),
):
    try:
        db.replace_user(uuid_, item)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='user not found',
        ) from exception

@router.patch(
    '/{uuid_}',
    summary='Alters an user',
    description='Alters an user identified by its UUID',
)
async def alter_user(
        uuid_: uuid.UUID,
        item: User,
        db: DBSession = Depends(get_db),
):
    try:
        old_item = db.fetch_user(uuid_)
        update_data = item.dict(exclude_unset=True)
        new_item = old_item.copy(update=update_data)
        db.replace_user(uuid_, new_item)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        ) from exception

@router.delete(
    '/{uuid_}',
    summary='Deletes an user',
    description='Deletes an user identified by its UUID',
)
async def remove_user(uuid_: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        db.remove_user(uuid_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        ) from exception
