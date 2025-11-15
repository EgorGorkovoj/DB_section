from sqlalchemy import String, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from schema_db.models.db import Base
from schema_db.core.constants import LengthConstants


class City(Base):
    name_city: Mapped[str] = mapped_column(
        String(LengthConstants.TITLE_LENGTH), nullable=False, unique=True
    )
    days_delivery: Mapped[int] = mapped_column(
        SmallInteger, nullable=False
    )

    clients: Mapped[list['Client']] = relationship(
        'Client',
        back_populates='city',
        passive_deletes=True
    )

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}(id={self.id}, '
            f'name_city={self.name_city}, '
            f'days_delivery={self.days_delivery})>'
        )


class Client(Base):
    name_client: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey('city.id', ondelete='SET NULL'), nullable=True
    )
    email: Mapped[str | None] = mapped_column(
        String(LengthConstants.EMAIL_LENGTH), unique=True, nullable=True
    )

    city: Mapped['City'] = relationship(
        'City',
        back_populates='clients'
    )

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}(id={self.id}, '
            f'name_city={self.name_client}, '
            f'city_id={self.city_id}, email={self.email})>'
        )
