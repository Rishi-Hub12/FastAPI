from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    age: int
    city: str


class UserUpdate(BaseModel):
    name: str
    age: int
    city: str


class UserPatch(BaseModel):
    name: str | None = None
    age: int | None = None
    city: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    city: str

    class Config:
        from_attributes = True