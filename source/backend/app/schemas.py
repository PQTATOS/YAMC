from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    username: str
    is_admin: bool

class UserRegSchema(BaseModel):
    username: str
    password: str


class ServerSchema(BaseModel):
    id: int
    user_id: int
    cloud_vm_name: str