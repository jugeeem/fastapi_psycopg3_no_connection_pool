from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    description: str


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    id: int


class TodoRead(TodoBase):
    id: int
