from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    username: str
    is_admin: bool

class UserRegSchema(BaseModel):
    username: str
    password: str
