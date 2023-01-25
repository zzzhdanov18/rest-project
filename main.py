from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from core.models.database import Base, engine, get_db
from typing import List
from uuid import uuid4, UUID
import core.models.models as models
import core.schemas.schema as sh


app = FastAPI()

Base.metadata.create_all(engine)


@app.get("/api/v1/menus", response_model=List[sh.Menu])
def get_all_menus(db: Session = Depends(get_db)):
    menus = db.query(models.Menu).all()
    for item in menus:
        item.submenus_count = db.query(models.Submenu).filter_by(id_menu=item.id).count()
        item.dishes_count = db.query(models.Submenu).join(models.Dish).filter(models.Submenu.id_menu == item.id).count()
    db.commit()
    return menus


@app.get("/api/v1/menus/{menu_id}", response_model=sh.Menu)
def get_a_menu(menu_id: UUID, db: Session = Depends(get_db)):
    q_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if q_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    q_menu.submenus_count = db.query(models.Submenu).filter_by(id_menu=q_menu.id).count()
    q_menu.dishes_count = db.query(models.Submenu).join(models.Dish).filter(models.Submenu.id_menu == q_menu.id).count()
    db.commit()
    return q_menu


@app.post("/api/v1/menus", response_model=sh.Menu, status_code=status.HTTP_201_CREATED)
def create_menu(menu: sh.Menu, db: Session = Depends(get_db)):
    new_menu = models.Menu(
        id=uuid4(),
        title=menu.title,
        description=menu.description,
        submenus_count=0,
        dishes_count=0
    )
    db.add(new_menu)
    db.commit()

    return new_menu


@app.patch("/api/v1/menus/{menu_id}", response_model=sh.Menu)
def update_menu(menu_id: UUID, menu: sh.Menu, db: Session = Depends(get_db)):
    menu_to_update = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if menu_to_update is None:
        raise HTTPException(status_code=400, detail="menu not found")
    menu_to_update.title = menu.title
    menu_to_update.description = menu.description
    menu_to_update.submenus_count = db.query(models.Submenu).filter_by(id_menu=menu_to_update.id).count()
    menu_to_update.dishes_count = db.query(models.Submenu).join(models.Dish).\
        filter(models.Submenu.id_menu == menu_to_update.id).count()

    db.commit()
    return menu_to_update


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: UUID, db: Session = Depends(get_db)):
    db.query(models.Menu).filter(models.Menu.id == menu_id).delete()
    db.commit()
    return {"status": "true",
            "message": "The menu has been deleted"
            }


#######################################################################################

@app.get("/api/v1/menus/{id_menu}/submenus", response_model=List[sh.Submenu])
def get_all_submenus(id_menu: UUID, db: Session = Depends(get_db)):
    submenus = db.query(models.Submenu).filter(models.Submenu.id_menu == id_menu).all()
    for item in submenus:
        item.dishes_count = db.query(models.Dish).filter_by(id_submenu=item.id).count()
    db.commit()
    return submenus


@app.get("/api/v1/menus/{id_menu}/submenus/{id_sub}", response_model=sh.Submenu)
def get_submenu(id_sub: UUID, db: Session = Depends(get_db)):
    q_sub = db.query(models.Submenu).filter(models.Submenu.id == id_sub).first()
    if q_sub is None:
        raise HTTPException(status_code=404, detail="submenu not found")
        return

    q_sub.dishes_count = db.query(models.Dish).filter_by(id_submenu=q_sub.id).count()
    db.commit()
    return q_sub


@app.post("/api/v1/menus/{id_menu_f}/submenus", response_model=sh.Submenu, status_code=status.HTTP_201_CREATED)
def create_submenu(id_menu_f: UUID, submenu: sh.Submenu, db: Session = Depends(get_db)):
    new_sub = models.Submenu(
        id=uuid4(),
        id_menu=id_menu_f,
        title=submenu.title,
        description=submenu.description,
        dishes_count=0
    )
    db.add(new_sub)
    db.commit()
    return new_sub


@app.patch("/api/v1/menus/{id_menu_f}/submenus/{id_sub}", response_model=sh.Submenu)
def update_submenu(id_sub: UUID, submenu: sh.Submenu, db: Session = Depends(get_db)):
    sub_to_update = db.query(models.Submenu).filter(models.Submenu.id == id_sub).first()

    if sub_to_update is None:
        raise HTTPException(status_code=400, detail="submenu not found")
        return

    sub_to_update.title = submenu.title
    sub_to_update.description = submenu.description
    sub_to_update.dishes_count = db.query(models.Dish).filter_by(id_submenu=sub_to_update.id).count()

    db.commit()
    return sub_to_update


@app.delete("/api/v1/menus/{id_menu_f}/submenus/{id_sub}")
def delete_submenu(id_sub: UUID, db: Session = Depends(get_db)):

    db.query(models.Submenu).filter(models.Submenu.id == id_sub).delete()
    db.commit()
    return {"status": "true",
            "message": "The submenu has been deleted"
            }


############################################################################################


@app.get("/api/v1/menus/{id_menu}/submenus/{id_sub}/dishes", response_model=List[sh.Dish])
def get_all_dishes(id_sub: UUID, db: Session = Depends(get_db)):
    return db.query(models.Dish).filter(models.Dish.id_submenu == id_sub).all()


@app.get("/api/v1/menus/{id_menu}/submenus/{id_sub}/dishes/{id_dish}", response_model=sh.Dish)
def get_dish(id_menu: str, id_sub: UUID, id_dish: UUID, db: Session = Depends(get_db)):
    q_dish = db.query(models.Dish).filter(models.Dish.id == id_dish).filter(models.Dish.id_submenu == id_sub).first()
    if q_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return q_dish


@app.post("/api/v1/menus/{id_menu}/submenus/{id_sub}/dishes", response_model=sh.Dish, status_code=status.HTTP_201_CREATED)
def create_dish(id_sub: UUID, dish: sh.Dish, db: Session = Depends(get_db)):
    new_dish = models.Dish(
        id=uuid4(),
        id_submenu=id_sub,
        title=dish.title,
        description=dish.description,
        price=dish.price
    )
    db.add(new_dish)
    db.commit()

    return new_dish


@app.patch("/api/v1/menus/{id_menu}/submenus/{id_sub}/dishes/{id_dish}", response_model=sh.Dish)
def update_dish(id_sub: UUID, id_dish: UUID, dish: sh.Dish, db: Session = Depends(get_db)):
    dish_to_update = db.query(models.Dish).filter(models.Dish.id == id_dish).filter(
        models.Dish.id_submenu == id_sub).first()
    if dish_to_update is None:
        raise HTTPException(status_code=400, detail="dish not found")
    dish_to_update.title = dish.title
    dish_to_update.description = dish.description
    dish_to_update.price = dish.price

    db.commit()
    return dish_to_update


@app.delete("/api/v1/menus/{id_menu}/submenus/{id_sub}/dishes/{id_dish}")
def delete_dish(id_sub: UUID, id_dish: UUID, db: Session = Depends(get_db)):
    db.query(models.Dish).filter(models.Dish.id == id_dish).filter(models.Dish.id_submenu == id_sub).delete()
    db.commit()
    return {"status": "true",
            "message": "The dish has been deleted"
            }



