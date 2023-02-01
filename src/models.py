from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    description = Column(String(1000), nullable=True)
    relating_submenu = relationship(
        'SubMenu', lazy='joined', back_populates='relating_menu', cascade='delete',
    )


class SubMenu(Base):
    __tablename__ = 'submenu'

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, ForeignKey('menu.id', ondelete='CASCADE'))
    relating_menu = relationship('Menu', lazy='joined')
    relating_dish = relationship(
        'Dish', lazy='joined', back_populates='relating_sm', cascade='delete',
    )
    title = Column(String(100), unique=True, nullable=False)
    description = Column(String(1000), nullable=True)


#
#
class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True)
    submenu_id = Column(Integer, ForeignKey('submenu.id', ondelete='CASCADE'))
    relating_sm = relationship('SubMenu', lazy='joined')
    title = Column(String(100), unique=True, nullable=False)
    description = Column(String(1000), nullable=True)
    price = Column(Float)
