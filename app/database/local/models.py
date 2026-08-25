from datetime import date

from sqlalchemy import String, Date,DateTime,Text
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
        nullable=False,
        unique=True
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

class EsocialDesligamento(Base):
    __tablename__="esocial_desligamento"
    id:Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    matricula:Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    cpf:Mapped[str] = mapped_column(
        String(11),
        nullable=False
    )
    tipo_evento:Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    status:Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default='PENDENTE'
    )
    id_evento:Mapped[str|None] = mapped_column(
        String(100),
        nullable=True
    )
    xml:Mapped[str|None] =mapped_column(
        Text,
        nullable=True
    )
    recibo:Mapped[str|None] = mapped_column(
        String(100),
        nullable=True
    )
    data_envio:Mapped[DateTime|None] =mapped_column(
        DateTime,
        nullable=True

    )
    data_retorno:Mapped[DateTime|None] = mapped_column(
        DateTime,
        nullable=True
    )
    mensagem_erro:Mapped[str|None] = mapped_column(
        Text,
        nullable=True
    )
