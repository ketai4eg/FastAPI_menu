import http

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
@menu_app.get(
    path='/api/v1/menus/{menu_id}',
    response_model=schemas.MenuOut,
    summary='Any specific menu',
    status_code=status.HTTP_200_OK,
    responses={
        404: {'description': 'menu not found'},
        422: {'description': 'Validation Error'},
    },
)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    """Obtaining any specific menu by ID"""
    return crud.get_menus_info(db, menu_id)


# get menu list
@menu_app.get(
    path='/api/v1/menus/',
    response_model=list[schemas.MenuOut],
    summary='Full list of menus',
    status_code=http.HTTPStatus.OK,
)
def get_menus_list(db: Session = Depends(get_db)):
    """Obtaining full menus list"""
    return crud.get_menus_info(db)


# create menu
@menu_app.post(
    '/api/v1/menus/',
    response_model=schemas.Menu,
    status_code=status.HTTP_201_CREATED,
    summary='New menu creation',
    responses={
        400: {'description': 'submenu already existed'},
        422: {'description': 'Validation Error'},
    },
)
def create_menu(menu: schemas.MenuBase, db: Session = Depends(get_db)):
    """Creation of new menu"""
    crud.get_orm_item_by_name(Menu, db, title=menu.title)
    return crud.create_menu(db=db, menu=menu)


@menu_app.patch(
    '/api/v1/menus/{menu_id}',
    response_model=schemas.Menu,
    summary='Updating any meny by ID',
    status_code=http.HTTPStatus.OK,
    responses={
        404: {'description': 'menu not found'},
        422: {'description': 'Validation Error'},
    },
)
def patch_menu(menu_id: int | None, new_menu: schemas.MenuUpdate, db: Session = Depends(get_db)):
    """Use menu ID for update the menu information"""
    old_menu = crud.get_orm_item(Menu, menu_id, db)
    new_menu_data = new_menu.dict(exclude_unset=True)
    return crud.update_menu(db, old_menu, new_menu_data)


@menu_app.delete(
    '/api/v1/menus/{menu_id}',
    summary='Removing of any meny by ID',
    status_code=http.HTTPStatus.OK,
    responses={
        404: {'description': 'menu not found'},
    },
)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """Use ID for removing of any menu"""
    menu = crud.get_orm_item(Menu, menu_id, db)
    return crud.delete_item(db, menu, layer='menu')


@menu_app.post(
    '/api/v1/menus/{menu_id}/submenus/',
    response_model=schemas.SubMenuBase,
    status_code=status.HTTP_201_CREATED,
    summary='New menu creation',
    responses={
        400: {'description': 'submenu already existed'},
        404: {'description': 'menu not found'},
        422: {'description': 'Validation Error'},
    },
)
def create_submenu(submenu: schemas.SubMenuCreation, menu_id: int, db: Session = Depends(get_db)):
    """creation of the submenu for specific menu (by ID)"""
    crud.get_orm_item_by_name(SubMenu, db, title=submenu.title)
    return crud.create_submenu(db=db, menu_id=menu_id, submenu=submenu)


@menu_app.get(
    '/api/v1/menus/{menu_id}/submenus/',
    response_model=list[schemas.SubMenuOut],
    status_code=http.HTTPStatus.OK,
    summary='Full submenu list',
    responses={
        404: {'description': 'menu not found'},
    },
)
def get_submenu_list(menu_id: int, db: Session = Depends(get_db)):
    """Obtaining full list of submenu for specific menu by ID"""
    crud.get_orm_item(Menu, menu_id, db)
    return crud.get_submenus_list(db=db, item_id=menu_id)


@menu_app.get(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    response_model=schemas.SubMenuOut,
    status_code=http.HTTPStatus.OK,
    summary='Specific submenu by ID',
    responses={
        404: {'description': 'menu not found'},
    },
)
def get_submenu_info(submenu_id: int, db: Session = Depends(get_db)):
    """obtaining specific submenu by ID"""
    return crud.get_submenu_info(db, submenu_id)


@menu_app.patch(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    response_model=schemas.SubMenuBase,
    summary='Submenu updating',
    responses={
        400: {'description': 'submenu already existed'},
        404: {'description': 'menu not found'},
        422: {'description': 'Validation Error'},
    },
)
def patch_submenu(submenu_id: int | None, new_menu: schemas.SubMenuUpdate, db: Session = Depends(get_db)):
    """ update any submenu by ID"""
    old_menu = crud.get_orm_item(SubMenu, submenu_id, db)
    new_menu_data = new_menu.dict(exclude_unset=True)
    return crud.update_submenu(db, old_menu, new_menu_data)


@menu_app.delete(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    summary='Removing of any submenu by ID',
    status_code=http.HTTPStatus.OK,
    responses={
        404: {'description': 'submenu not found'},
    },
)
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    """Removing any submenu by its ID"""
    submenu = crud.get_orm_item(SubMenu, submenu_id, db)
    return crud.delete_item(db, submenu, layer='submenu', menu_id=menu_id)


@menu_app.post(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=schemas.DishesReturn,
    summary='Dish creating for specific submenu by ID',
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {'description': 'dish already existed'},
        404: {'description': 'submenu not found'},
        422: {'description': 'Validation Error'},
    },
)
def create_dish(submenu_id: int, dish: schemas.DishesBase, db: Session = Depends(get_db)):
    """Creation of dish for specific submenu by id"""
    crud.get_orm_item_by_name(Dish, db, title=dish.title)
    return crud.create_dish(db=db, submenu_id=submenu_id, dish=dish)


@menu_app.get(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=schemas.DishesReturn,
    summary='Specific dish description request (by ID)',
    status_code=status.HTTP_200_OK,
    responses={
        404: {'description': 'dish not found'},
    },
)
def get_dish_by_id(dish_id: int, db: Session = Depends(get_db)):
    """Request of the dish description by dish ID"""
    return crud.get_dish(Dish, dish_id, db)


@menu_app.get(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[schemas.DishesReturn],
    status_code=status.HTTP_200_OK,
    summary='Full dishes list for specific submenu (by submenu id)',
    responses={
        404: {'description': 'menu not found'},
    },
)
def get_dishes(submenu_id: int, db: Session = Depends(get_db)):
    """Obtaining of the dishes list for specific submenu by submenu ID"""
    return crud.get_dishes_list(db=db, submenu_id=submenu_id)


@menu_app.patch(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=schemas.DishesReturn,
    summary='Dish updating',
    responses={
        400: {'description': 'dish already existed'},
        404: {'description': 'dish not found'},
        422: {'description': 'Validation Error'},
    },
)
def patch_dish(dish_id: int | None, new_dish: schemas.DishUpdate, db: Session = Depends(get_db)):
    """Updating dish information by dish ID"""
    old_dish = crud.get_orm_item(Dish, dish_id, db)
    new_dish_data = new_dish.dict(exclude_unset=True)
    return crud.update_dish(db, old_dish, new_dish_data)


@menu_app.delete(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    summary='Removing of any dish',
    status_code=http.HTTPStatus.OK,
    responses={
        404: {'description': 'dish not found'},
    },
)
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    """Removing any dish"""
    dish = crud.get_orm_item(Dish, dish_id, db)
    return crud.delete_item(db, dish, layer='dish', menu_id=menu_id, submenu_id=submenu_id)
