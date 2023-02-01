from core.db.db_config import Base
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String(30), nullable=False, unique=True)
    description = Column(String(50))
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(UUID(as_uuid=True), primary_key=True)
    id_menu = Column(UUID(as_uuid=True), ForeignKey(
        'menu.id', ondelete='CASCADE'))
    title = Column(String(30), nullable=False)
    description = Column(String(50))
    dishes_count = Column(Integer, default=0)


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(UUID(as_uuid=True), primary_key=True)
    id_submenu = Column(
        UUID(as_uuid=True), ForeignKey('submenu.id', ondelete='CASCADE')
    )
    title = Column(String(30), nullable=False)
    description = Column(String(50))
    price = Column(String, default=0)
