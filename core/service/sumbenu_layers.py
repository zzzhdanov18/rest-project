from uuid import uuid4
from fastapi import HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from core.schemas.schema import *
import core.models.models as models
from core.service.templates import AbstractService, AbstractCRUD, AbstractSessionContext
from core.db.db_config import get_db
from core.db.db import PostgresDB


class SubmenusCRUD(AbstractCRUD):
    def get_list(self, id_menu: UUID):
        submenus = self.db.exec().query(models.Submenu).filter(models.Submenu.id_menu == id_menu).all()
        for item in submenus:
            item.dishes_count = self.db.exec().query(models.Dish).filter_by(id_submenu=item.id).count()
        self.db.commit()
        return submenus

    def get_detail(self, id_sub: UUID):
        q_sub = self.db.exec().query(models.Submenu).filter(models.Submenu.id == id_sub).first()
        if q_sub is None:
            return None
        q_sub.dishes_count = self.db.exec().query(models.Dish).filter_by(id_submenu=q_sub.id).count()
        self.db.commit()
        return q_sub

    def create(self, id_menu_f: UUID, submenu: SubmenuItemCreate):
        new_sub = models.Submenu(
            id=uuid4(),
            id_menu=id_menu_f,
            title=submenu.title,
            description=submenu.description,
            dishes_count=0
        )
        self.db.add(new_sub)
        self.db.commit()
        return new_sub

    def update(self, id_sub: UUID, submenu: SubmenuItemCreate):
        sub_to_update = self.db.exec().query(models.Submenu).filter(models.Submenu.id == id_sub).first()

        if sub_to_update is None:
            return None

        sub_to_update.title = submenu.title
        sub_to_update.description = submenu.description
        sub_to_update.dishes_count = self.db.exec().query(models.Dish).filter_by(id_submenu=sub_to_update.id).count()

        self.db.commit()
        return sub_to_update

    def delete(self, id_sub: UUID):
        self.db.exec().query(models.Submenu).filter(models.Submenu.id == id_sub).delete()
        self.db.commit()


#############################################################################################################

class SubmenuService(AbstractService):

    def get_list_of_items(self, menu_id: UUID) -> list[SubmenuItem]:
        list_items = self.crud_controller.get_list(menu_id)
        return list_items

    def get_item(self, submenu_id: UUID) -> SubmenuItem:
        item = self.crud_controller.get_detail(submenu_id)
        if item is None:
            raise HTTPException(status_code=404, detail='submenu not found')
        return item

    def create_item(self, menu_id: UUID, submenu: SubmenuItemCreate) -> SubmenuItem:
        item = self.crud_controller.create(menu_id, submenu)
        return item

    def update_item(self, submenu_id: UUID, update: SubmenuItemCreate) -> SubmenuItem:
        item = self.crud_controller.update(submenu_id, update)
        if item is None:
            raise HTTPException(status_code=400, detail='submenu not found')
        return item

    def delete_item(self, submenu_id: UUID):
        self.crud_controller.delete(submenu_id)
        return {
            'status': 'true',
            'message': 'The submenu has been deleted'
        }


def get_submenu_service(session: Session = Depends(get_db)) -> AbstractService:
    db_context: AbstractSessionContext = PostgresDB(session)
    crud_controller: AbstractCRUD = SubmenusCRUD(db_context)
    submenu_service: AbstractService = SubmenuService(crud_controller)

    return submenu_service
