import hashlib
import os
import base64
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie

from database import get_session
from schemas import UserRegSchema
from database import User
from config import SALT_SIZE

auth_router = APIRouter(prefix="/auth", tags=["auth"])

active_hashes = {}

@auth_router.post("/registrate")
async def registrate_user(
    user_reg: UserRegSchema,
    resp: Response,
    db_session: AsyncSession = Depends(get_session)
):
    
    if await db_session.scalar(
        select(User)
        .where(User.username == user_reg.username)
        ) is not None:
        raise HTTPException(status_code=401)
    
    salt = os.urandom(SALT_SIZE)
    key = hashlib.pbkdf2_hmac('sha256', user_reg.password.encode('utf-8'), salt, 100000)
    hash = base64.b64encode(salt + key).decode()
    user_db = User(username=user_reg.username, hashed_password=hash, is_admin=False)
    
    db_session.add(user_db)
    await db_session.commit()

    active_hashes[user_db.id] = uuid4().hex

    resp.set_cookie(key="token", value=active_hashes[user_db.id])
    resp.set_cookie(key="user_id", value=user_db.id)
    return f'{user_db.id}'


@auth_router.post("/login")
async def login(
    user_reg: UserRegSchema,
    resp: Response,
    db_session: AsyncSession = Depends(get_session)
):
    if (db_user := await db_session.scalar(
        select(User)
        .where(User.username == user_reg.username)
        )) is None:
        raise HTTPException(status_code=404)
    
    decoded = base64.b64decode(db_user.hashed_password.encode())
    salt = decoded[:SALT_SIZE]
    key = decoded[SALT_SIZE:]
    pswd = hashlib.pbkdf2_hmac('sha256', user_reg.password.encode('utf-8'), salt, 100000) 
    
    if pswd != key:
        raise HTTPException(status_code=401)
    
    active_hashes[db_user.id] = uuid4().hex

    resp.set_cookie(key="token", value=active_hashes[db_user.id])
    resp.set_cookie(key="user_id", value=db_user.id)
    return f'{db_user.id}'


async def get_current_user(
    resp: Response,
    user_id: int | None = Cookie(default=None),
    token: str | None = Cookie(default=None),
    db_session: AsyncSession = Depends(get_session)
):
    if user_id is None or token is None:
        raise HTTPException(status_code=401)
    if token != active_hashes.get(user_id, 0):
        raise HTTPException(status_code=401)
    return await db_session.scalar(select(User).where(User.id == user_id))
    