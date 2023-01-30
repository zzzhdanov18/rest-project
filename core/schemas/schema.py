from pydantic import BaseModel
from uuid import UUID


class BaseItemModel(BaseModel):
    title: str
    description: str


class MenuItemCreate(BaseItemModel):
    pass


class MenuItem(BaseItemModel):
    id: UUID
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class SubmenuItemCreate(BaseItemModel):
    pass


class SubmenuItem(BaseItemModel):
    id: UUID
    dishes_count: int

    class Config:
        orm_mode = True


class DishItemCreate(BaseItemModel):
    price: str


class DishItem(DishItemCreate):
    id: UUID

    class Config:
        orm_mode = True
