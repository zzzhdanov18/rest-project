from uuid import uuid4
from fastapi import HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from core.schemas.schema import *
import core.models.models as models
from core.service.templates import AbstractService, AbstractCRUD, AbstractSessionContext
from core.db.db_config import get_db
from core.db.db import PostgresDB


class MenusCRUD(AbstractCRUD):

    def get_list(self):
        menus = self.db.exec().query(models.Menu).all()
        for item in menus:
            item.submenus_count = self.db.exec().query(models.Submenu).filter_by(id_menu=item.id).count()
            item.dishes_count = self.db.exec().query(models.Submenu).join(models.Dish).filter(
                models.Submenu.id_menu == item.id).count()
        self.db.commit()
        return menus

    def get_detail(self, menu_id: UUID):
        q_menu = self.db.exec().query(models.Menu).filter(models.Menu.id == menu_id).first()
        if q_menu is None:
            return None
        q_menu.submenus_count = self.db.exec().query(models.Submenu).filter_by(id_menu=q_menu.id).count()
        q_menu.dishes_count = self.db.exec().query(models.Submenu).join(models.Dish).filter(
            models.Submenu.id_menu == q_menu.id).count()
        self.db.commit()
        return q_menu

    def create(self, menu: MenuItemCreate):
        new_menu = models.Menu(
            id=uuid4(),
            title=menu.title,
            description=menu.description,
            submenus_count=0,
            dishes_count=0
        )
        self.db.add(new_menu)
        self.db.commit()
        return new_menu

    def update(self, menu_id: UUID, update_val: MenuItemCreate):
        menu_to_update = self.db.exec().query(models.Menu).filter(models.Menu.id == menu_id).first()
        if menu_to_update is None:
            return None

        menu_to_update.title = update_val.title
        menu_to_update.description = update_val.description
        menu_to_update.submenus_count = self.db.exec().query(models.Submenu).filter_by(id_menu=menu_to_update.id).count()
        menu_to_update.dishes_count = self.db.exec().query(models.Submenu).join(models.Dish). \
            filter(models.Submenu.id_menu == menu_to_update.id).count()

        self.db.commit()
        return menu_to_update

    def delete(self, menu_id: UUID):
        self.db.exec().query(models.Menu).filter(models.Menu.id == menu_id).delete()
        self.db.commit()


class MenuService(AbstractService):

    def get_list_of_items(self) -> list[MenuItem]:
        list_items = self.crud_controller.get_list()
        return list_items

    def get_item(self, menu_id: UUID) -> MenuItem:
        item = self.crud_controller.get_detail(menu_id)
        if item is None:
            raise HTTPException(status_code=404, detail='menu not found')
        return item

    def create_item(self, menu: MenuItemCreate) -> MenuItem:
        item = self.crud_controller.create(menu)
        return item

    def update_item(self, menu_id: UUID, update: MenuItemCreate) -> MenuItem:
        item = self.crud_controller.update(menu_id, update)
        if item is None:
            raise HTTPException(status_code=400, detail='menu not found')
        return item

    def delete_item(self, menu_id: UUID):
        self.crud_controller.delete(menu_id)
        return {
            'status': 'true',
            'message': 'The menu has been deleted'
        }


def get_menu_service(session: Session = Depends(get_db)) -> AbstractService:
    db_context: AbstractSessionContext = PostgresDB(session)
    crud_controller: AbstractCRUD = MenusCRUD(db_context)
    menu_service: AbstractService = MenuService(crud_controller)
    return menu_service
