from pydantic import BaseModel
from uuid import UUID


class Menu(BaseModel):
    id: UUID = None
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        orm_mode = True


class Submenu(BaseModel):
    id: UUID = None
    title: str
    description: str
    dishes_count: int = None

    class Config:
        orm_mode = True


class Dish(BaseModel):
    id: UUID = None
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True
