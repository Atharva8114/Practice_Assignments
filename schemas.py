from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = None
