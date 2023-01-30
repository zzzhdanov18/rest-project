# from abc import ABC, abstractmethod
# from uuid import uuid4
#
# from sqlalchemy.orm import Session
# from fastapi import Depends, HTTPException
# from core.db.db_config import get_db
# from core.models import models
# from core.schemas.schema import *
# from typing import List, Optional
#
#
# class AbstractSessionContext(ABC):
#     db: Optional
#
#     @abstractmethod
#     def commit(self):
#         raise NotImplementedError
#
#     @abstractmethod
#     def rollback(self):
#         raise NotImplementedError
#
#     @abstractmethod
#     def add(self):
#         raise NotImplementedError
#
#     @abstractmethod
#     def exec(self):
#         raise NotImplementedError
#
#
# class PostgresDB(AbstractSessionContext):
#     db: Session
#
#     def __init__(self, db):
#         self.db = db
#
#     def commit(self):
#         self.db.commit()
#
#     def rollback(self):
#         self.db.rollback()
#
#     def add(self, arg):
#         self.db.add(arg)
#
#     def exec(self):
#         return self.db
#
#
# class AbstractCRUD(ABC):
#
#     db: AbstractSessionContext
#
#     def __init__(self, db):
#         self.db = db
#
#     @abstractmethod
#     def get_list(self,*args, **kwargs):
#         raise NotImplementedError
#
#     @abstractmethod
#     def get_detail(self,*args, **kwargs):
#         raise NotImplementedError
#
#     @abstractmethod
#     def create(self,*args, **kwargs):
#         raise NotImplementedError
#
#     @abstractmethod
#     def update(self,*args, **kwargs):
#         raise NotImplementedError
#
#     @abstractmethod
#     def delete(self, *args, **kwargs):
#         raise NotImplementedError
#
#
# class MenusCRUD(AbstractCRUD):
#
#     def get_list(self):
#         menus = self.db.exec().query(models.Menu).all()
#         for item in menus:
#             item.submenus_count = self.db.exec().query(models.Submenu).filter_by(id_menu=item.id).count()
#             item.dishes_count = self.db.exec().query(models.Submenu).join(models.Dish).filter(
#                 models.Submenu.id_menu == item.id).count()
#         self.db.commit()
#         return menus
#
#     def get_detail(self, menu_id: UUID):
#         q_menu = self.db.exec().query(models.Menu).filter(models.Menu.id == menu_id).first()
#         if q_menu is None:
#             return None
#         q_menu.submenus_count = self.db.exec().query(models.Submenu).filter_by(id_menu=q_menu.id).count()
#         q_menu.dishes_count = self.db.exec().query(models.Submenu).join(models.Dish).filter(
#             models.Submenu.id_menu == q_menu.id).count()
#         self.db.commit()
#         return q_menu
#
#     def create(self, menu: MenuItemCreate):
#         new_menu = models.Menu(
#             id=uuid4(),
#             title=menu.title,
#             description=menu.description,
#             submenus_count=0,
#             dishes_count=0
#         )
#         self.db.add(new_menu)
#         self.db.commit()
#         return new_menu
#
#     def update(self, menu_id: UUID, update_val: MenuItemCreate):
#         menu_to_update = self.db.exec().query(models.Menu).filter(models.Menu.id == menu_id).first()
#         if menu_to_update is None:
#             return None
#
#         menu_to_update.title = update_val.title
#         menu_to_update.description = update_val.description
#         menu_to_update.submenus_count = self.db.exec().query(models.Submenu).filter_by(id_menu=menu_to_update.id).count()
#         menu_to_update.dishes_count = self.db.exec().query(models.Submenu).join(models.Dish). \
#             filter(models.Submenu.id_menu == menu_to_update.id).count()
#
#         self.db.commit()
#         return menu_to_update
#
#     def delete(self, menu_id: UUID):
#         self.db.exec().query(models.Menu).filter(models.Menu.id == menu_id).delete()
#         self.db.commit()
#
#
# class AbstractService(ABC):
#
#     crud_controller: AbstractCRUD
#
#     def __init__(self, crud_controller):
#         self.crud_controller = crud_controller
#
#     @abstractmethod
#     def get_list_of_items(self, *args, **kwargs):
#         raise NotImplementedError
#
#     @abstractmethod
#     def get_item(self,*args, **kwargs):
#         raise NotImplementedError
#
#     @abstractmethod
#     def create_item(self, *args, **kwargs):
#         raise NotImplementedError
#
#     @abstractmethod
#     def update_item(self, *args, **kwargs):
#         raise NotImplementedError
#
#     @abstractmethod
#     def delete_item(self, *args, **kwargs):
#         raise NotImplementedError
#
#
# class MenuService(AbstractService):
#
#     def get_list_of_items(self) -> List[MenuItem]:
#         list_items = self.crud_controller.get_list()
#         return list_items
#
#     def get_item(self, menu_id: UUID) -> MenuItem:
#         item = self.crud_controller.get_detail(menu_id)
#         if item is None:
#             raise HTTPException(status_code=404, detail="menu not found")
#         return item
#
#     def create_item(self, menu: MenuItemCreate) -> MenuItem:
#         item = self.crud_controller.create(menu)
#         return item
#
#     def update_item(self, menu_id: UUID, update: MenuItemCreate) -> MenuItem:
#         item = self.crud_controller.update(menu_id, update)
#         if item is None:
#             raise HTTPException(status_code=400, detail="menu not found")
#         return item
#
#     def delete_item(self, menu_id: UUID):
#         self.crud_controller.delete(menu_id)
#         return {
#             "status": "true",
#             "message": "The menu has been deleted"
#         }
#
#
# def get_menu_service(session: Session = Depends(get_db)) -> AbstractService:
#     db_context: AbstractSessionContext = PostgresDB(session)
#     crud_controller: AbstractCRUD = MenusCRUD(db_context)
#     menu_service: AbstractService = MenuService(crud_controller)
#     return menu_service
#
#
# class SubmenusCRUD(AbstractCRUD):
#     def get_list(self, id_menu: UUID):
#         submenus = self.db.exec().query(models.Submenu).filter(models.Submenu.id_menu == id_menu).all()
#         for item in submenus:
#             item.dishes_count = self.db.exec().query(models.Dish).filter_by(id_submenu=item.id).count()
#         self.db.commit()
#         return submenus
#
#     def get_detail(self, id_sub: UUID):
#         q_sub = self.db.exec().query(models.Submenu).filter(models.Submenu.id == id_sub).first()
#         if q_sub is None:
#             return None
#         q_sub.dishes_count = self.db.exec().query(models.Dish).filter_by(id_submenu=q_sub.id).count()
#         self.db.commit()
#         return q_sub
#
#     def create(self, id_menu_f: UUID, submenu: SubmenuItemCreate):
#         new_sub = models.Submenu(
#             id=uuid4(),
#             id_menu=id_menu_f,
#             title=submenu.title,
#             description=submenu.description,
#             dishes_count=0
#         )
#         self.db.add(new_sub)
#         self.db.commit()
#         return new_sub
#
#     def update(self, id_sub: UUID, submenu: SubmenuItemCreate):
#         sub_to_update = self.db.exec().query(models.Submenu).filter(models.Submenu.id == id_sub).first()
#
#         if sub_to_update is None:
#             return None
#
#         sub_to_update.title = submenu.title
#         sub_to_update.description = submenu.description
#         sub_to_update.dishes_count = self.db.exec().query(models.Dish).filter_by(id_submenu=sub_to_update.id).count()
#
#         self.db.commit()
#         return sub_to_update
#
#     def delete(self, id_sub: UUID):
#         self.db.exec().query(models.Submenu).filter(models.Submenu.id == id_sub).delete()
#         self.db.commit()
#
#
# class SubmenuService(AbstractService):
#
#     def get_list_of_items(self, menu_id: UUID) -> List[SubmenuItem]:
#         list_items = self.crud_controller.get_list(menu_id)
#         return list_items
#
#     def get_item(self, submenu_id: UUID) -> SubmenuItem:
#         item = self.crud_controller.get_detail(submenu_id)
#         if item is None:
#             raise HTTPException(status_code=404, detail="submenu not found")
#         return item
#
#     def create_item(self, menu_id: UUID, submenu: SubmenuItemCreate) -> SubmenuItem:
#         item = self.crud_controller.create(menu_id, submenu)
#         return item
#
#     def update_item(self, submenu_id: UUID, update: SubmenuItemCreate) -> SubmenuItem:
#         item = self.crud_controller.update(submenu_id, update)
#         if item is None:
#             raise HTTPException(status_code=400, detail="submenu not found")
#         return item
#
#     def delete_item(self, submenu_id: UUID):
#         self.crud_controller.delete(submenu_id)
#         return {
#             "status": "true",
#             "message": "The submenu has been deleted"
#         }
#
#
# def get_submenu_service(session: Session = Depends(get_db)) -> AbstractService:
#     db_context: AbstractSessionContext = PostgresDB(session)
#     crud_controller: AbstractCRUD = SubmenusCRUD(db_context)
#     submenu_service: AbstractService = SubmenuService(crud_controller)
#
#     return submenu_service
#
#
# class DishesCRUD(AbstractCRUD):
#     def get_list(self, id_sub: UUID):
#         items_list = self.db.exec().query(models.Dish).filter(models.Dish.id_submenu == id_sub).all()
#         return items_list
#
#     def get_detail(self, id_sub: UUID, id_dish:UUID):
#         q_dish = self.db.exec().query(models.Dish).filter(models.Dish.id == id_dish).filter(
#             models.Dish.id_submenu == id_sub).first()
#         if q_dish is None:
#             return None
#         return q_dish
#
#     def create(self, id_sub: UUID, dish: DishItemCreate):
#         new_dish = models.Dish(
#             id=uuid4(),
#             id_submenu=id_sub,
#             title=dish.title,
#             description=dish.description,
#             price=dish.price
#         )
#         self.db.add(new_dish)
#         self.db.commit()
#
#         return new_dish
#
#     def update(self, id_sub: UUID, id_dish: UUID, dish: DishItemCreate):
#         dish_to_update = self.db.exec().query(models.Dish).filter(models.Dish.id == id_dish).filter(
#             models.Dish.id_submenu == id_sub).first()
#         if dish_to_update is None:
#             return None
#
#         dish_to_update.title = dish.title
#         dish_to_update.description = dish.description
#         dish_to_update.price = dish.price
#
#         self.db.commit()
#         return dish_to_update
#
#     def delete(self, id_sub: UUID, id_dish: UUID):
#         self.db.exec().query(models.Dish).filter(models.Dish.id == id_dish).filter(models.Dish.id_submenu == id_sub).delete()
#         self.db.commit()
#
#
# class DishService(AbstractService):
#     def get_list_of_items(self, id_sub: UUID) -> List[DishItem]:
#         return self.crud_controller.get_list(id_sub)
#
#     def get_item(self, id_sub: UUID, id_dish:UUID) -> DishItem:
#         item = self.crud_controller.get_detail(id_sub, id_dish)
#         if item is None:
#             raise HTTPException(status_code=404, detail="dish not found")
#         return item
#
#     def create_item(self, id_sub: UUID, dish: DishItemCreate) -> DishItem:
#         item = self.crud_controller.create(id_sub, dish)
#         return item
#
#     def update_item(self, id_sub: UUID, id_dish: UUID, dish: DishItemCreate) -> DishItem:
#         item = self.crud_controller.update(id_sub, id_dish, dish)
#         if item is None:
#             raise HTTPException(status_code=400, detail="dish not found")
#         return item
#
#     def delete_item(self, id_sub: UUID, id_dish: UUID):
#         self.crud_controller.delete(id_sub, id_dish)
#         return {
#             "status": "true",
#             "message": "The dish has been deleted"
#         }
#
#
# def get_dish_service(session: Session = Depends(get_db)) -> AbstractService:
#     db_context: AbstractSessionContext = PostgresDB(session)
#     crud_controller: AbstractCRUD = DishesCRUD(db_context)
#     dish_service: AbstractService = DishService(crud_controller)
#
#     return dish_service

from core.service.templates import AbstractSessionContext
from sqlalchemy.orm import Session


class PostgresDB(AbstractSessionContext):
    db: Session

    def __init__(self, db):
        self.db = db

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def add(self, arg):
        self.db.add(arg)

    def exec(self):
        return self.db
