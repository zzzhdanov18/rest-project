import json
from uuid import uuid4, UUID
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from redis.client import Redis

from core.schemas.schema import DishItemCreate, DishItem
import core.models.models as models
from core.service.templates import (
    AbstractService,
    AbstractCRUD,
    AbstractSessionContext,
    AbstractCache,
)
from core.db.db_config import get_db
from core.cache.cache_config import get_cache
from core.db.db import PostgresDB
from core.cache.redis_cache import RedisCache


class DishesCRUD(AbstractCRUD):
    def get_list(self, id_sub: UUID):
        items_list = (
            self.db.exec()
            .query(models.Dish)
            .filter(models.Dish.id_submenu == id_sub)
            .all()
        )
        return items_list

    def get_detail(self, id_sub: UUID, id_dish: UUID):
        q_dish = (
            self.db.exec()
            .query(models.Dish)
            .filter(models.Dish.id == id_dish)
            .filter(models.Dish.id_submenu == id_sub)
            .first()
        )
        if q_dish is None:
            return None
        return q_dish

    def create(self, id_sub: UUID, dish: DishItemCreate):
        new_dish = models.Dish(
            id=uuid4(),
            id_submenu=id_sub,
            title=dish.title,
            description=dish.description,
            price=dish.price,
        )

        self.db.add(new_dish)
        self.db.commit()

        return new_dish

    def update(self, id_sub: UUID, id_dish: UUID, dish: DishItemCreate):
        dish_to_update = self.get_detail(id_sub, id_dish)
        if dish_to_update is None:
            return None
        dish_to_update.title = dish.title
        dish_to_update.description = dish.description
        dish_to_update.price = dish.price

        self.db.commit()
        return dish_to_update

    def delete(self, id_sub: UUID, id_dish: UUID):
        self.db.exec().query(models.Dish).filter(models.Dish.id == id_dish).filter(
            models.Dish.id_submenu == id_sub
        ).delete()
        self.db.commit()


class DishService(AbstractService):
    def get_item(self, id_sub: UUID, id_dish: UUID) -> DishItem:
        if self.cache.get(str(id_dish)):
            return json.loads(self.cache.get(str(id_dish)))

        item = self.crud_controller.get_detail(id_sub, id_dish)
        if item is None:
            raise HTTPException(status_code=404, detail='dish not found')

        to_cache = self.serialize_for_cache(item)
        self.cache.set(to_cache['id'], json.dumps(to_cache))

        return item

    def create_item(
        self, id_menu: UUID, id_sub: UUID, dish: DishItemCreate
    ) -> DishItem:
        item = self.crud_controller.create(id_sub, dish)

        to_cache = self.serialize_for_cache(item)
        self.cache.set(to_cache['id'], json.dumps(to_cache))
        self.cache.delete(str(id_menu))
        self.cache.delete(str(id_sub))

        return item

    def update_item(
        self, id_sub: UUID, id_dish: UUID, dish: DishItemCreate
    ) -> DishItem:
        item = self.crud_controller.update(id_sub, id_dish, dish)
        if item is None:
            raise HTTPException(status_code=400, detail='dish not found')

        to_cache = self.serialize_for_cache(item)
        self.cache.set(to_cache['id'], json.dumps(to_cache))

        return item

    def delete_item(self, id_menu: UUID, id_sub: UUID, id_dish: UUID):
        self.crud_controller.delete(id_sub, id_dish)

        self.cache.delete(str(id_dish))
        self.cache.delete(str(id_menu))
        self.cache.delete(str(id_sub))

        return {'status': 'true', 'message': 'The dish has been deleted'}

    def get_list_of_items(self, id_sub: UUID) -> list[DishItem]:
        return self.crud_controller.get_list(id_sub)

    def serialize_for_cache(self, dish: models.Dish):
        data = {
            'id': str(dish.id),
            'title': dish.title,
            'description': dish.description,
            'price': dish.price,
        }
        return data


def get_dish_service(
    session: Session = Depends(get_db), redis: Redis = Depends(get_cache)
) -> AbstractService:
    db_context: AbstractSessionContext = PostgresDB(session)
    cache_context: AbstractCache = RedisCache(redis)
    crud_controller: AbstractCRUD = DishesCRUD(db_context)
    dish_service: AbstractService = DishService(crud_controller, cache_context)

    return dish_service
