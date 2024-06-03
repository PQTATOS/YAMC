import requests
from uuid import uuid4
import asyncio

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import User, Server
from schemas import ServerSchema
from auth import get_current_user, get_session
from config import SUBNET_ID, IAM_TOKEN, FOLDER_ID

server_router = APIRouter(prefix="/servers", tags=["server"])


@server_router.post("/add")
async def add_server(
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session)
):
    while True:
        server_name = f"vm-{uuid4().hex}"

        server = await db_session.scalar(
            select(Server).where(Server.cloud_vm_name == server_name)
        )

        if server is None:
            break
    
    server = Server(user_id=user.id, cloud_vm_name=server_name, srever_map_link=server_name)
    
    headers={"Authorization": f"Bearer {IAM_TOKEN}"}
    data = f'{{"folderId": "{FOLDER_ID}","name": "{server_name}","zoneId": "ru-central1-a","platformId": "standard-v3","resourcesSpec": {{"memory": "4294967296","cores": "2","coreFraction": "100"}},"bootDiskSpec": {{"diskSpec": {{"size": "19327352832","imageId": "fd8606smtda8ncrvctfh"}}}},"networkInterfaceSpecs": [{{"subnetId": "{SUBNET_ID}","primaryV4AddressSpec": {{"oneToOneNatSpec": {{"ipVersion": "IPV4"}}}}}}]}}'
    print(data)
    req = requests.post(
        "https://compute.api.cloud.yandex.net/compute/v1/instances",
        headers=headers,
        data=data
    )

    print(req.status_code, req.text)
    
    db_session.add(server)
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