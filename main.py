from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from models import Menu, SubMenu, Dish

from database import SessionLocal, engine

import schemas
import crud
import models

models.Base.metadata.create_all(bind=engine)
menu_app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# get menu by ID
@menu_app.get("/api/v1/menus/{menu_id}", response_model=schemas.MenuOut)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    return crud.get_menus_info(db, menu_id)


# get menu list
@menu_app.get("/api/v1/menus/", response_model=list[schemas.MenuOut])
def get_menus_list(db: Session = Depends(get_db)):
    return crud.get_menus_info(db)


# create menu
@menu_app.post("/api/v1/menus/", response_model=schemas.Menu, status_code=status.HTTP_201_CREATED)
def create_menu(menu: schemas.MenuBase, db: Session = Depends(get_db)):
    crud.get_orm_item_by_name(Menu, db, title=menu.title)
    return crud.create_menu(db=db, menu=menu)


@menu_app.patch("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def patch_menu(menu_id: int | None, new_menu: schemas.MenuUpdate, db: Session = Depends(get_db)):
    old_menu = crud.get_orm_item(Menu, menu_id, db)
    new_menu_data = new_menu.dict(exclude_unset=True)
    return crud.update_menu(db, old_menu, new_menu_data)


@menu_app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = crud.get_orm_item(Menu, menu_id, db)
    return crud.delete_item(db, menu)


@menu_app.post("/api/v1/menus/{menu_id}/submenus/", response_model=schemas.SubMenuBase,
               status_code=status.HTTP_201_CREATED)
def create_submenu(submenu: schemas.SubMenuCreation, menu_id: int, db: Session = Depends(get_db)):
    crud.get_orm_item_by_name(SubMenu, db, title=submenu.title)
    return crud.create_submenu(db=db, menu_id=menu_id, submenu=submenu)


@menu_app.get("/api/v1/menus/{menu_id}/submenus/", response_model=list[schemas.SubMenuOut])
def get_submenu_list(menu_id: int, db: Session = Depends(get_db)):
    crud.get_orm_item(Menu, menu_id, db)
    return crud.get_submenus_list(db=db, item_id=menu_id)


@menu_app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenuOut)
def get_submenu_info(submenu_id: int, db: Session = Depends(get_db)):
    return crud.get_submenu_info(db, submenu_id)


@menu_app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenuBase)
def patch_submenu(submenu_id: int | None, new_menu: schemas.SubMenuUpdate, db: Session = Depends(get_db)):
    old_menu = crud.get_orm_item(SubMenu, submenu_id, db)
    new_menu_data = new_menu.dict(exclude_unset=True)
    return crud.update_menu(db, old_menu, new_menu_data)


@menu_app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(submenu_id: int, db: Session = Depends(get_db)):
    submenu = crud.get_orm_item(SubMenu, submenu_id, db)
    return crud.delete_item(db, submenu)


@menu_app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=schemas.DishesReturn,
               status_code=status.HTTP_201_CREATED)
def create_dish(submenu_id: int, dish: schemas.DishesBase, db: Session = Depends(get_db)):
    crud.get_orm_item_by_name(Dish, db, title=dish.title)
    return crud.create_dish(db=db, submenu_id=submenu_id, dish=dish)


@menu_app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.DishesReturn)
def get_dish_by_id(dish_id: int, db: Session = Depends(get_db)):
    return crud.get_orm_item(Dish, dish_id, db)


@menu_app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[schemas.DishesReturn])
def get_submenu_by_id(submenu_id: int, db: Session = Depends(get_db)):
    return crud.get_dishes_list(db=db, submenu_id=submenu_id)


@menu_app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.DishesReturn)
def patch_dish(dish_id: int | None, new_dish: schemas.DishUpdate, db: Session = Depends(get_db)):
    old_dish = crud.get_orm_item(Dish, dish_id, db)
    new_dish_data = new_dish.dict(exclude_unset=True)
    return crud.update_dish(db, old_dish, new_dish_data)


@menu_app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = crud.get_orm_item(Dish, dish_id, db)
    return crud.delete_item(db, dish)
