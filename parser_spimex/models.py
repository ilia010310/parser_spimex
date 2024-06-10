from datetime import datetime, timezone
from typing import Annotated

from sqlalchemy import MetaData, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from database import Base

int_pk = Annotated[int, mapped_column(primary_key=True)]



class SpimexTradingResults(Base):
    __tablename__ = 'spimex_trading_results'

    id: Mapped[int_pk]
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[int]
    total: Mapped[int]
    count: Mapped[int]
    date: Mapped[datetime] = mapped_column(DateTime)
    created_on: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc)
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )
