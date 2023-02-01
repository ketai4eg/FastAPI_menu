from pydantic import BaseModel, Field
from typing import Optional


class TempMenu(BaseModel):
    title: str
    id: int
    description: str | None
    submenus_count: int
    dishes_count: int
    relating_submenu: Optional[list] = None


class MenuOut(BaseModel):
    title: str = Field(
        title='Menu title',
        max_length=100,
    )
    id: str
    description: str | None
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        schema_extra = {
            'example': {
                'title': 'Breakfast',
                'description': 'Something light',
                'menu id': '5',
                'submenu_count': 5,
                'dishes_count': 3,
            },
        }


class MenuBase(BaseModel):
    title: str
    description: str | None

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Breakfast',
                'description': 'Something light',
            },
        }


class Menu(MenuBase):
    id: str

    class Config:
        schema_extra = {
            'example': {
                'title': 'Breakfast',
                'description': 'Something light',
                'id': '5',
            },
        }


class MenuUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Breakfast',
                'description': 'Something light',
                'id': '5',
            },
        }


class SubMenuCreation(BaseModel):
    title: str
    description: str | None

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Blin4iki',
                'description': 'Round and fried',
                'id': '5',
            },
        }


class TempSubMenu(BaseModel):
    title: str
    id: int
    description: str | None
    dishes_count: int
    relating_dish: Optional[list] = None


class SubMenuOut(BaseModel):
    title: str
    id: str
    description: str | None
    dishes_count: int = 0

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Blin4iki',
                'description': 'Round and fried',
                'id': '5',
                'dishes_count': 7,
            },
        }


class SubMenuBase(SubMenuCreation):
    id: str
    menu_id: str


class SubMenuUpdate(SubMenuCreation):
    title: str
    description: Optional[str] = None


class DishesBase(BaseModel):
    title: str
    description: str | None
    price: float

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Blin4iki',
                'description': 'Round and fried',
                'price': 5.7,
            },
        }


class DishesReturn(BaseModel):
    title: str
    description: str | None
    price: str
    id: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Blin4iki',
                'description': 'Round and fried',
                'price': '5.7',
                'id': '7',
            },
        }


class DishUpdate(DishesBase):
    title: str
    description: Optional[str] = None
    price: float

    class Config:
        schema_extra = {
            'example': {
                'title': 'Blin4iki',
                'description': 'Round and fried',
                'price': '50.7',
                'id': '7',
            },
        }
