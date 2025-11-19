import datetime

from sqlalchemy import and_, select
from .crud_base import CRUDBase
from model import SpamixTradingResults

from sqlalchemy.orm import Session


class TradeCRUD(CRUDBase):
    """
    Класс для работы с моделью 'SpamixTradingResults' через CRUD операции.
    Наследуется от CRUDBase, расширяя функциональность проверкой существующих записей.

    Методы:
        exists_exchange_product_id(session, exchange_product_id, date)
            Проверяет, существует ли запись с указанным 'exchange_product_id' и 'date'.
    """
    def exists_exchange_product_id(
        self, session: Session,
        exchange_product_id: str,
        date: datetime.date
    ) -> SpamixTradingResults | None:
        """
        Проверяет наличие записи в базе.

        Параметры:
            session (Session): Активная сессия SQLAlchemy.
            exchange_product_id (str): Идентификатор продукта на бирже.
            date (datetime.date): Дата сделки.

        Возвращает:
            SpamixTradingResults | None: Объект модели, если запись найдена, иначе None.
        """
        result = select(SpamixTradingResults).where(
            and_(
                SpamixTradingResults.exchange_product_id == exchange_product_id,
                SpamixTradingResults.date == date
            )
        )
        return session.execute(result).scalars().first()


crud_trade = TradeCRUD(SpamixTradingResults)
