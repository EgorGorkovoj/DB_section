from typing import TYPE_CHECKING
from datetime import datetime
from enum import StrEnum

from sqlalchemy import TIMESTAMP, Enum, Text, ForeignKey, SmallInteger, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from schema_db.core.constants import DefaultValueConstants
from .db import Base

if TYPE_CHECKING:
    from book import Book


class StepStatus(StrEnum):
    """Варианты значения поля name_step в модели Step."""

    PROCESSING = 'В обработке'
    PAID = 'Оплачено'
    SHIPPED = 'Отправлено'
    DELIVERED = 'Доставлено'
    CANCELED = 'Отменено'


class Buy(Base):

    buy_description: Mapped[str] = mapped_column(Text, nullable=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey('client.id', ondelete='CASCADE'), nullable=False
    )

    books: Mapped[list['BuyBook']] = relationship(
        'BuyBook',
        back_populates='buy',
        cascade='all, delete-orphan'
    )
    steps: Mapped[list['BuyStep']] = relationship(
        'BuyStep',
        back_populates='buy',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}(id={self.id}, '
            f'buy_description={self.buy_description}, '
            f'client_id={self.client_id})> '
        )


class BuyBook(Base):

    buy_id: Mapped[int] = mapped_column(
        ForeignKey('buy.id', ondelete='CASCADE'), nullable=False
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey('book.id', ondelete='RESTRICT'), nullable=False
    )
    amount: Mapped[int] = mapped_column(
        SmallInteger, default=DefaultValueConstants.AMOUNT, nullable=False
    )

    buy: Mapped['Buy'] = relationship(
        'Buy',
        back_populates='books'
    )

    book: Mapped['Book'] = relationship(
        'Book',
        back_populates='buy_items'
    )

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}(id={self.id}, '
            f'buy_id={self.buy_id}, book_id={self.book_id}, '
            f'amount={self.amount})> '
        )


class Step(Base):
    name_step: Mapped['StepStatus'] = mapped_column(
        Enum(StepStatus, name='stepstatus'),
        default=StepStatus.PROCESSING,
        nullable=False
    )

    buy_steps: Mapped[list['BuyStep']] = relationship(
        'BuyStep',
        back_populates='step'
    )

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}(id={self.id}, '
            f'buyname_step_id={self.name_step})>'
        )


class BuyStep(Base):

    buy_id: Mapped[int] = mapped_column(
        ForeignKey('buy.id', ondelete='CASCADE'), nullable=False
    )
    step_id: Mapped[int] = mapped_column(
        ForeignKey('step.id'), nullable=False
    )
    date_step_beg: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    date_step_end: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True
    )

    buy: Mapped['Buy'] = relationship(
        'Buy',
        back_populates='steps'
    )

    step: Mapped['Step'] = relationship(
        'Step',
        back_populates='buy_steps'
    )

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}(id={self.id}, '
            f'buy_id={self.buy_id}, step_id={self.step_id}, '
            f'date_step_beg={self.date_step_beg}, '
            f'date_step_end={self.date_step_end})> '
        )
