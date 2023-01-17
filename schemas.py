from pydantic import BaseModel
from typing import Optional


class TempMenu(BaseModel):
    title: str
    id: int
    description: str | None
    submenus_count: int
    dishes_count: int
    relating_submenu: Optional[list] = None


class MenuOut(BaseModel):
    title: str
    id: str
    description: str | None
    submenus_count: int
    dishes_count: int = 0


class MenuBase(BaseModel):
    title: str
    description: str | None

    class Config:
        orm_mode = True


class Menu(MenuBase):
    id: str
    # submenus: List['SubMenuBase']


class MenuUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class SubMenuCreation(BaseModel):
    title: str
    description: str | None

    class Config:
        orm_mode = True


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


class SubMenuBase(SubMenuCreation):
    id: str
    menu_id: str


class SubMenuUpdate(SubMenuCreation):
    title: Optional[str] = None
    description: Optional[str] = None


class DishesBase(BaseModel):
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True


class DishesReturn(DishesBase):
    price: str
    id: str


class DishUpdate(DishesBase):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
