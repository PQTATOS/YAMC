from subprocess import Popen, PIPE
from uuid import uuid4
import asyncio

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import User, Server
from app.schemas import ServerSchema
from app.auth import get_current_user, get_session
from app.config import SUBNET_ID

server_router = APIRouter(prefix="/servers", tags=["server"])


@server_router.post("/add")
async def add_server(
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session)
):
    while True:
        server_name = uuid4().hex

        server = await db_session.scalar(
            select(Server).where(Server.cloud_vm_name == server_name)
        )

        if server is None:
            break
    
    server = Server(user_id=user.id, cloud_vm_name=server_name)

    task = f"yc compute instance create --name {server_name} --zone ru-central1-a --network-interface subnet-id={SUBNET_ID},nat-ip-version=ipv4"
    proc = Popen(task,shell=True, stderr=PIPE, stdout=PIPE)
    
    while True:
        retcode = proc.poll()
        if retcode is None:
            await asyncio.sleep(5)
        else:
            break
    
    await db_session.add(server)
    await db_session.commit()

    return server_name


@server_router.get("/")
async def get_servers(
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session)
):
    servers = await db_session.scalars(
        select(Server)
        .where(Server.user_id == user.id)
    )

    return [ServerSchema.model_validate(server, from_attributes=True) for server in servers]


@server_router.post("/delete")
async def delete_server(
    server_name: str = Query(),
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session)
):
    server = await db_session.scalar(
        select(Server)
        .where(Server.user_id == user.id)
        .where(Server.cloud_vm_name == server_name)
    )

    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    
    db_session.delete(server)
    await db_session.commit()

    return "ok"