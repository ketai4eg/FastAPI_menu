from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload
import models
import schemas
import cache


def get_menus_info(db: Session, object_id: int | None = None):
    if object_id is None:

        menus = db.query(models.Menu).options(
            joinedload(models.Menu.relating_submenu).joinedload(
                models.SubMenu.relating_dish,
            ),
        ).all()
        list_menu = []
        for menu in menus:
            dishes_count = 0
            submenu = jsonable_encoder(menu)['relating_submenu']
            for dish in submenu:
                dishes_count += len(dish['relating_dish'])
            menu = schemas.TempMenu(
                **jsonable_encoder(menu),
                submenus_count=len(jsonable_encoder(menu)['relating_submenu']),
                dishes_count=dishes_count,
            )
            list_menu.append(menu)
        menus = list[schemas.TempMenu](list_menu)
        return menus

    else:
        if cache.cache_get(object_id, 'menu'):
            return cache.cache_get(object_id, 'menu')
        item = db.query(models.Menu).options(
            joinedload(models.Menu.relating_submenu).joinedload(
                models.SubMenu.relating_dish,
            ),
        ).filter(
            models.Menu.id == object_id,
        ).first()
        if item is None:
            raise HTTPException(
                status_code=404, detail='menu not found'.lower(),
            )
        dishes_count = 0
        submenu = jsonable_encoder(item)['relating_submenu']
        for dish in submenu:
            dishes_count += len(dish['relating_dish'])
        item = schemas.TempMenu(
            **jsonable_encoder(item),
            submenus_count=len(jsonable_encoder(item)['relating_submenu']),
            dishes_count=dishes_count,
        )
        if item is None:
            raise HTTPException(
                status_code=404, detail='menu not found'.lower(),
            )
        cache.cache_set(item, 'menu')
        return item


def get_orm_item(orm_class, object_id, db):
    item = db.get(orm_class, object_id)
    if item is None:
        raise HTTPException(
            status_code=404, detail=f'{orm_class.__name__} not found'.lower(),
        )
    return item


def get_orm_item_by_name(orm_class, db: Session, title: str):
    db_menu = db.query(orm_class).filter(orm_class.title == title).first()
    if db_menu:
        raise HTTPException(
            status_code=400, detail=f'{orm_class.__name__} already existed'.lower(),
        )
    return 'ok'


def create_menu(db: Session, menu: schemas.MenuBase):
    new_menu = models.Menu(title=menu.title, description=menu.description)
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


def update_menu(db: Session, menu: schemas.MenuUpdate, new_menu_data):
    for key, value in new_menu_data.items():
        setattr(menu, key, value)
    db.add(menu)
    db.commit()
    db.refresh(menu)
    cache.cache_set(menu, 'menu')
    return menu


def delete_item(db: Session, item, layer, menu_id=None, submenu_id=None):
    info = jsonable_encoder(item)
    db.delete(item)
    db.commit()
    cache.cache_delete(info['id'], layer)
    try:
        cache.cache_delete(menu_id, layer='menu')
    finally:
        try:
            cache.cache_delete(submenu_id, layer='submenu')
        finally:
            return {'ok': True}


def get_submenu_by_name(db: Session, title: str):
    return db.query(models.SubMenu).filter(models.SubMenu.title == title).first()


def create_submenu(db: Session, menu_id, submenu: schemas.SubMenuCreation):
    new_submenu = models.SubMenu(
        menu_id=menu_id, title=submenu.title, description=submenu.description,
    )
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu


def get_submenus_list(db: Session, item_id: int):
    submenus = db.query(models.SubMenu).options(joinedload(models.SubMenu.relating_dish)).filter(
        models.SubMenu.menu_id == item_id,
    ).all()
    list_submenus = []
    if submenus is None:
        raise HTTPException(
            status_code=404, detail='submenu not found'.lower(),
        )
    for submenu in submenus:
        dishes_count = len(jsonable_encoder(submenu)['relating_dish'])
        submenu = schemas.TempSubMenu(
            **jsonable_encoder(submenu),
            dishes_count=dishes_count,
        )
        list_submenus.append(submenu)
    submenus = list[schemas.TempSubMenu](list_submenus)

    return submenus


def get_submenu_info(db: Session, item_id: int):
    if cache.cache_get(item_id, 'submenu'):
        return cache.cache_get(item_id, 'submenu')
    submenu = db.query(models.SubMenu).options(joinedload(models.SubMenu.relating_dish)).filter(
        models.SubMenu.id == item_id,
    ).first()
    if submenu is None:
        raise HTTPException(
            status_code=404, detail='submenu not found'.lower(),
        )
    dishes_count = len(jsonable_encoder(submenu)['relating_dish'])
    submenu = schemas.TempSubMenu(
        **jsonable_encoder(submenu),
        dishes_count=dishes_count,
    )
    cache.cache_set(submenu, 'submenu')
    return submenu


def update_submenu(db: Session, submenu: schemas.SubMenuUpdate, new_menu_data):
    for key, value in new_menu_data.items():
        setattr(submenu, key, value)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    cache.cache_set(submenu, layer='submenu')
    return submenu


def create_dish(db: Session, submenu_id: int, dish: schemas.DishesBase):
    new_dish = models.Dish(
        submenu_id=submenu_id, title=dish.title, description=dish.description,
        price=float('%.2f' % dish.price),
    )
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish


def get_dish(orm_class, object_id, db):
    if cache.cache_get(object_id, 'dish'):
        return cache.cache_get(object_id, 'dish')
    item = db.get(orm_class, object_id)
    if item is None:
        raise HTTPException(
            status_code=404, detail=f'{orm_class.__name__} not found'.lower(),
        )
    cache.cache_set(item, 'dish')
    return item


def get_dishes_list(db: Session, submenu_id: int):
    return db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all()


def update_dish(db: Session, dish: schemas.DishUpdate, new_dish_data):
    for key, value in new_dish_data.items():
        setattr(dish, key, value)
    db.add(dish)
    db.commit()
    db.refresh(dish)
    cache.cache_set(dish, 'dish')
    return dish
