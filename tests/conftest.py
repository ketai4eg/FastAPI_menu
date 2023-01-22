import pytest
import time
from models import Base, Menu, SubMenu, Dish
from config import PG_DSN
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


def new_menu_create():
    with Session() as session:
        new_menu = Menu(title=f'new_menu_{time.time()}', description='blablabla')
        session.add(new_menu)
        session.commit()
        return {
            'id': new_menu.id,
            'title': new_menu.title,
            'description': new_menu.description
        }


def new_submenu_create(menu_id):
    with Session() as session:
        new_submenu = SubMenu(title=f'new_submenu_{time.time()}', description='blablabla', menu_id=menu_id)
        session.add(new_submenu)
        session.commit()
        return {
            'id': new_submenu.id,
            'menu_id': new_submenu.menu_id,
            'title': new_submenu.title,
            'description': new_submenu.description
        }


def new_dish_create(submenu_id):
    with Session() as session:
        new_dish = Dish(title=f'new_dish_{time.time()}', description='blablabla', submenu_id=submenu_id, price=10.65)
        session.add(new_dish)
        session.commit()
        return {
            'id': new_dish.id,
            'submenu_id': new_dish.submenu_id,
            'title': new_dish.title,
            'description': new_dish.description,
            'price': new_dish.price
        }


@pytest.fixture(scope='session', autouse=True)
def cleanup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture(scope='session')
def root_menu():
    return new_menu_create()


@pytest.fixture(scope='session')
def root_submenu():
    menu = new_menu_create()
    return new_submenu_create(menu['id'])


@pytest.fixture(scope='session')
def root_dish():
    menu = new_menu_create()
    new_submenu = new_submenu_create(menu['id'])
    new_dish = new_dish_create(new_submenu['id'])
    new_dish['menu_id'] = menu['id']
    return new_dish


@pytest.fixture()
def new_menu():
    return new_menu_create()


@pytest.fixture()
def new_submenu():
    menu = new_menu_create()
    return new_submenu_create(menu['id'])


@pytest.fixture()
def new_dish():
    menu = new_menu_create()
    new_submenu = new_submenu_create(menu['id'])
    new_dish = new_dish_create(new_submenu['id'])
    new_dish['menu_id'] = menu['id']
    return new_dish
