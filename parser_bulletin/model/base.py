from sqlalchemy.orm import (DeclarativeBase, declared_attr,
                            Mapped, mapped_column)


class PreBase(DeclarativeBase):
    """Базовая модель проекта"""
    pass


class Base(PreBase):
    """
    Базовая модель проекта. Абстрактная модель.

    Задает наследникам имя таблицы в БД строчными буквами от названия модели.
    """

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
