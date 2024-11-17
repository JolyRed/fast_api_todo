from pydantic import BaseModel

class TodoItemBase(BaseModel):
    title: str
    description: str
    completed: bool = False

class TodoItemCreate(TodoItemBase):
    pass

class TodoItem(TodoItemBase):
    id: int

    class Config:
        from_attributes = True
