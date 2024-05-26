from fastapi import FastAPI, Depends

from auth import auth_router, get_current_user
from admin_panel import admin_router
from database import User

app = FastAPI()

app.include_router(auth_router)
app.include_router(admin_router)

@app.get("/")
async def home_page(
    user: User = Depends(get_current_user)
):
    return user.username