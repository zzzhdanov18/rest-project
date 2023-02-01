from fastapi import APIRouter, Depends
from fastapi import status
from uuid import UUID

from core.schemas.schema import (
    MenuItem,
    MenuItemCreate,
    SubmenuItem,
    SubmenuItemCreate,
    DishItem,
    DishItemCreate,
)

from core.service.menu_layers import get_menu_service
from core.service.dish_layers import get_dish_service
from core.service.sumbenu_layers import get_submenu_service
from core.service.templates import AbstractService


rest_router = APIRouter(prefix='/api/v1', tags=['menus'])


@rest_router.get('/menus', response_model=list[MenuItem])
def get_menus(menu_service: AbstractService = Depends(get_menu_service)):
    items = menu_service.get_list_of_items()
    return items


@rest_router.get('/menus/{menu_id}', response_model=MenuItem)
def get_a_menu(
    menu_id: UUID, menu_service: AbstractService = Depends(get_menu_service)
):
    item = menu_service.get_item(menu_id)
    return item


@rest_router.post(
    '/menus', response_model=MenuItem, status_code=status.HTTP_201_CREATED
)
def create_menu(
    menu: MenuItemCreate, menu_service: AbstractService = Depends(get_menu_service)
):
    item = menu_service.create_item(menu)
    return item


@rest_router.patch('/menus/{menu_id}', response_model=MenuItem)
def update_menu(
    menu_id: UUID,
    menu: MenuItemCreate,
    menu_service: AbstractService = Depends(get_menu_service),
):
    item = menu_service.update_item(menu_id, menu)
    return item


@rest_router.delete('/menus/{menu_id}')
def delete_menu(
    menu_id: UUID, menu_service: AbstractService = Depends(get_menu_service)
):
    menu_service.delete_item(menu_id)


#######################################################################################


@rest_router.get('/menus/{id_menu}/submenus', response_model=list[SubmenuItem])
def get_all_submenus(
    id_menu: UUID, submenu_service: AbstractService = Depends(get_submenu_service)
):
    submenus = submenu_service.get_list_of_items(id_menu)
    return submenus


@rest_router.get('/menus/{id_menu}/submenus/{id_sub}', response_model=SubmenuItem)
def get_submenu(
    id_sub: UUID, submenu_service: AbstractService = Depends(get_submenu_service)
):
    q_sub = submenu_service.get_item(id_sub)
    return q_sub


@rest_router.post(
    '/menus/{id_menu_f}/submenus',
    response_model=SubmenuItem,
    status_code=status.HTTP_201_CREATED,
)
def create_submenu(
    id_menu_f: UUID,
    submenu: SubmenuItemCreate,
    submenu_service: AbstractService = Depends(get_submenu_service),
):
    new_sub = submenu_service.create_item(id_menu_f, submenu)
    return new_sub


@rest_router.patch('/menus/{id_menu_f}/submenus/{id_sub}', response_model=SubmenuItem)
def update_submenu(
    id_sub: UUID,
    submenu: SubmenuItemCreate,
    submenu_service: AbstractService = Depends(get_submenu_service),
):
    sub_to_update = submenu_service.update_item(id_sub, submenu)
    return sub_to_update


@rest_router.delete('/menus/{id_menu_f}/submenus/{id_sub}')
def delete_submenu(
    id_menu_f: UUID,
    id_sub: UUID,
    submenu_service: AbstractService = Depends(get_submenu_service),
):
    submenu_service.delete_item(id_menu_f, id_sub)


############################################################################################


@rest_router.get(
    '/menus/{id_menu}/submenus/{id_sub}/dishes', response_model=list[DishItem]
)
def get_all_dishes(
    id_sub: UUID, dish_service: AbstractService = Depends(get_dish_service)
):
    return dish_service.get_list_of_items(id_sub)


@rest_router.get(
    '/menus/{id_menu}/submenus/{id_sub}/dishes/{id_dish}', response_model=DishItem
)
def get_dish(
    id_sub: UUID,
    id_dish: UUID,
    dish_service: AbstractService = Depends(get_dish_service),
):
    q_dish = dish_service.get_item(id_sub, id_dish)
    return q_dish


@rest_router.post(
    '/menus/{id_menu}/submenus/{id_sub}/dishes',
    response_model=DishItem,
    status_code=status.HTTP_201_CREATED,
)
def create_dish(
    id_menu: UUID,
    id_sub: UUID,
    dish: DishItemCreate,
    dish_service: AbstractService = Depends(get_dish_service),
):
    new_dish = dish_service.create_item(id_menu, id_sub, dish)
    return new_dish


@rest_router.patch(
    '/menus/{id_menu}/submenus/{id_sub}/dishes/{id_dish}', response_model=DishItem
)
def update_dish(
    id_sub: UUID,
    id_dish: UUID,
    dish: DishItemCreate,
    dish_service: AbstractService = Depends(get_dish_service),
):
    dish_to_update = dish_service.update_item(id_sub, id_dish, dish)
    return dish_to_update


@rest_router.delete('/menus/{id_menu}/submenus/{id_sub}/dishes/{id_dish}')
def delete_dish(
    id_menu: UUID,
    id_sub: UUID,
    id_dish: UUID,
    dish_service: AbstractService = Depends(get_dish_service),
):
    dish_service.delete_item(id_menu, id_sub, id_dish)
