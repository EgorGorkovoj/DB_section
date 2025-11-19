import datetime
from sqlalchemy.orm import Session
from core.logger import logger
from crud.crud_trade import crud_trade
from model import SpamixTradingResults
from services.objects_converter import SpimexRowConverter
import pandas as pd
from typing import Optional


class SpimexImporter:
    """
    Класс для импорта данных таблиц в базу данных.

    Отвечает за:
        - конвертацию строк pandas.DataFrame в формат ORM-модели;
        - проверку существования записей в БД;
        - вставку одиночных строк или массовую загрузку;
        - работу через CRUD-слой (TradeCRUD).

    Параметры:
        session (Session): Активная сессия SQLAlchemy, в рамках которой
            выполняются операции записи и проверки.
    """

    def __init__(self, session: Session):
        self.session = session
        self.crud = crud_trade

    def save_row(
            self, row: pd.Series, file_date: datetime.date
    ) -> Optional[SpamixTradingResults]:
        """
        Сохраняет одну строку данных в таблицу БД.

        Алгоритм:
            1. Конвертирует строку DataFrame в словарь данных модели.
            2. Подставляет дату файла (file_date).
            3. Проверяет, есть ли уже запись с таким exchange_product_id и date.
            4. Если запись существует — ничего не добавляет.
            5. Если нет — создаёт новую запись через CRUD.

        Параметры:
            row (pd.Series): Строка DataFrame.
            file_date (datetime.date): Дата, которая будет сохранена в поле date.

        Возвращает:
            SpamixTradingResults | None:
                - объект модели, если запись создана;
                - None, если запись уже существует.
        """
        obj_data = SpimexRowConverter.convert_to_dict(row)

        obj_data['date'] = file_date

        exists = self.crud.exists_exchange_product_id(
            session=self.session,
            exchange_product_id=obj_data['exchange_product_id'],
            date=file_date
        )

        if exists:
            logger.info(f'Запись {exists} уже есть в БД!')
            return None

        return self.crud.create(self.session, obj_data=obj_data)

    def save_table_bulk(
            self, df: pd.DataFrame, file_date: datetime.date
    ) -> list[SpamixTradingResults] | None:
        """
        Выполняет массовую загрузку данных из DataFrame в БД.

        Алгоритм:
            1. Итерирует строки DataFrame.
            2. Конвертирует каждую строку в словарь данных модели.
            3. Устанавливает дату (file_date).
            4. Проверяет существование записи по exchange_product_id + date.
            5. Формирует список только новых записей.
            6. Массово сохраняет их в БД через bulk_create().

        Параметры:
            df (pd.DataFrame): Таблица данных после парсинга XML/XLS.
            file_date (datetime.date): Дата торгов, применяемая ко всем строкам.

        Возвращает:
            list[SpamixTradingResults] | None:
                - список созданных объектов, если были добавлены новые записи;
                - None, если все записи уже существовали.
        """
        objs_data = []
        for _, row in df.iterrows():
            obj_data = SpimexRowConverter.convert_to_dict(row)
            obj_data['date'] = file_date

            if not self.crud.exists_exchange_product_id(
                session=self.session,
                exchange_product_id=obj_data['exchange_product_id'],
                date=file_date
            ):
                objs_data.append(obj_data)

        if not objs_data:
            return None

        return self.crud.bulk_create(self.session, objs_data)
