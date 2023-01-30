from uuid import uuid4
from fastapi import HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from core.schemas.schema import *
import core.models.models as models
from core.service.templates import AbstractService, AbstractCRUD, AbstractSessionContext
from core.db.db_config import get_db
from core.db.db import PostgresDB


class DishesCRUD(AbstractCRUD):
    def get_list(self, id_sub: UUID):
        items_list = self.db.exec().query(models.Dish).filter(models.Dish.id_submenu == id_sub).all()
        return items_list

    def get_detail(self, id_sub: UUID, id_dish:UUID):
        q_dish = self.db.exec().query(models.Dish).filter(models.Dish.id == id_dish).filter(
            models.Dish.id_submenu == id_sub).first()
        if q_dish is None:
            return None
        return q_dish

    def create(self, id_sub: UUID, dish: DishItemCreate):
        new_dish = models.Dish(
            id=uuid4(),
            id_submenu=id_sub,
            title=dish.title,
            description=dish.description,
            price=dish.price
        )
        self.db.add(new_dish)
        self.db.commit()

        return new_dish

    def update(self, id_sub: UUID, id_dish: UUID, dish: DishItemCreate):
        dish_to_update = self.db.exec().query(models.Dish).filter(models.Dish.id == id_dish).filter(
            models.Dish.id_submenu == id_sub).first()
        if dish_to_update is None:
            return None

        dish_to_update.title = dish.title
        dish_to_update.description = dish.description
        dish_to_update.price = dish.price

        self.db.commit()
        return dish_to_update

    def delete(self, id_sub: UUID, id_dish: UUID):
        self.db.exec().query(models.Dish).filter(models.Dish.id == id_dish).filter(models.Dish.id_submenu == id_sub).delete()
        self.db.commit()


class DishService(AbstractService):
    def get_list_of_items(self, id_sub: UUID) -> list[DishItem]:
        return self.crud_controller.get_list(id_sub)

    def get_item(self, id_sub: UUID, id_dish:UUID) -> DishItem:
        item = self.crud_controller.get_detail(id_sub, id_dish)
        if item is None:
            raise HTTPException(status_code=404, detail='dish not found')
        return item

    def create_item(self, id_sub: UUID, dish: DishItemCreate) -> DishItem:
        item = self.crud_controller.create(id_sub, dish)
        return item

    def update_item(self, id_sub: UUID, id_dish: UUID, dish: DishItemCreate) -> DishItem:
        item = self.crud_controller.update(id_sub, id_dish, dish)
        if item is None:
            raise HTTPException(status_code=400, detail='dish not found')
        return item

    def delete_item(self, id_sub: UUID, id_dish: UUID):
        self.crud_controller.delete(id_sub, id_dish)
        return {
            'status': 'true',
            'message': 'The dish has been deleted'
        }


def get_dish_service(session: Session = Depends(get_db)) -> AbstractService:
    db_context: AbstractSessionContext = PostgresDB(session)
    crud_controller: AbstractCRUD = DishesCRUD(db_context)
    dish_service: AbstractService = DishService(crud_controller)

    return dish_service
