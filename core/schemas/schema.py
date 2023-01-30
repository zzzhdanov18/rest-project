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


# class Menu(BaseModel):
#     id: UUID = None
#     title: str
#     description: str
#     submenus_count: int = 0
#     dishes_count: int = 0
#
#     class Config:
#         orm_mode = True
#
#
# class Submenu(BaseModel):
#     id: UUID = None
#     title: str
#     description: str
#     dishes_count: int = None
#
#     class Config:
#         orm_mode = True
#
#
# class Dish(BaseModel):
#     id: UUID = None
#     title: str
#     description: str
#     price: str
#
#     class Config:
#         orm_mode = True
