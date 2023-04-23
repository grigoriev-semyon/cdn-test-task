from sqlalchemy import DECIMAL, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class City(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    lat: Mapped[float] = mapped_column(DECIMAL, nullable=False)
    lon: Mapped[float] = mapped_column(DECIMAL, nullable=False)
