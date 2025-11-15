from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Numeric, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base
from schema_db.core.constants import (LengthConstants,
                                      PriceConstants,
                                      DefaultValueConstants)

if TYPE_CHECKING:
    from buy import BuyBook


class Genre(Base):

    name_genre: Mapped[str] = mapped_column(
        String(LengthConstants.TITLE_LENGTH), nullable=False, unique=True
    )

    books: Mapped[list['Book']] = relationship('Book', back_populates='genre')

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}(id={self.id}, '
            f'name_genre={self.name_genre})>'
        )


class Author(Base):

    name_author: Mapped[str] = mapped_column(
        String(LengthConstants.TITLE_LENGTH), nullable=False, unique=True
    )

    books: Mapped[list['Book']] = relationship('Book', back_populates='author')

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}(id={self.id}, '
            f'name_author={self.name_author})>'
        )


class Book(Base):

    title: Mapped[str] = mapped_column(String(LengthConstants.TITLE_LENGTH), nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey('author.id', ondelete='RESTRICT')
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey('genre.id', ondelete='RESTRICT')
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(
            PriceConstants.PRICE_NUMBER_OF_DIGITS,
            PriceConstants.PRICE_FRACTIONAL_PART
        ),
        nullable=False
    )
    amount: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, default=DefaultValueConstants.AMOUNT
    )

    genre: Mapped['Genre'] = relationship('Genre', back_populates='books')
    author: Mapped['Author'] = relationship('Author', back_populates='books')
    buy_items: Mapped[list['BuyBook']] = relationship(
        'BuyBook',
        back_populates='book'
    )

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}(id={self.id}, '
            f'title={self.title}, author_id={self.author_id}, '
            f'genre_id={self.genre_id}, price={self.price}, '
            f'amount={self.amount})>'
        )
