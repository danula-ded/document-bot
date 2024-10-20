from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.model.meta import Base


class Gift(Base):
    __tablename__ = 'gift'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(index=True)
    category: Mapped[str] = mapped_column(String)
    photo: Mapped[str] = mapped_column(Text)
