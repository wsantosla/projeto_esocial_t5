from datetime import date

from sqlalchemy import String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class StgDesligamento(Base):
    __tablename__ = "stg_desligamento"

    id:Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    matricula: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    cpf: Mapped[str] = mapped_column(
        String(11),
        nullable=False
    )

    data_afastamento: Mapped[date | None] = mapped_column(
        Date,
        nullable=False
    )

    codigo_pmjp: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    descricao: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    codigo_esocial: Mapped[str] = mapped_column(
        String,
        nullable=False
    )