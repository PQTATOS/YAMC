from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session, User
from schemas import UserRegSchema, UserSchema
from auth import get_current_user

admin_router = APIRouter(prefix="/admin", tags=["admin"])

@admin_router.get("/users")
async def get_users(
    offset: int = Query(ge=0, default=0),
    admin: User = Depends(get_current_user),
    db_sesion: AsyncSession = Depends(get_session)
):
    if not admin.is_admin:
        raise HTTPException(status_code=403)
    
    users = await db_sesion.scalars(select(User).offset(offset).limit(10))

    return [UserSchema.model_validate(user, from_attributes=True) for user in users]

@admin_router.post("/users/delete")
async def delete_user(
    user_id: int = Query(),
    admin: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session)
):
    if not admin.is_admin:
        raise HTTPException(status_code=403)
    user = await db_session.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db_session.delete(user)
    await db_session.commit()

    return "ok"
