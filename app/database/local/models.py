from datetime import date, datetime

from sqlalchemy import String, Date, DateTime, Text, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class StgDesligamento(Base):
    __tablename__ = "stg_desligamento"

    id: Mapped[int] = mapped_column(
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

    data_afastamento: Mapped[date] = mapped_column(
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
    __tablename__ = "esocial_desligamento"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    protocolo_envio:Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    matricula: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    cpf_trab: Mapped[str] = mapped_column(
        String(11),
        nullable=False
    )

    dt_deslig: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    mtv_deslig: Mapped[str] = mapped_column(
        String(2),
        nullable=False
    )

    ind_pagto_api: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N"
    )

    # Controle do evento
    tipo_evento: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="S-2299"
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="PENDENTE"
    )

    id_evento: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    # XML assinado
    xml: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    recibo: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    data_envio: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    data_retorno: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    mensagem_erro: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


class EsocialControleId(Base):
    __tablename__ = "esocial_controle_id"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    tp_insc: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )

    nr_insc: Mapped[str] = mapped_column(
        String(14),
        nullable=False
    )

    data_hora: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    sequencial: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

class EsocialInfoEmpregador(Base):
    __tablename__ = "esocial_info_empregador"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    # Dados cadastrais do empregador
    tp_insc: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )

    nr_insc: Mapped[str] = mapped_column(
        String(14),
        nullable=False
    )

    ini_valid: Mapped[str] = mapped_column(
        String(7),
        nullable=False
    )

    class_trib: Mapped[str] = mapped_column(
        String(2),
        nullable=False
    )

    ind_coop: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )

    ind_constr: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )

    ind_des_folha: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )

    ind_opt_reg_eletron: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )

    cnpj_efr: Mapped[str | None] = mapped_column(
        String(14),
        nullable=True
    )

    # Controle do evento
    tipo_evento: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="S-1000"
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="PENDENTE"
    )

    id_evento: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        unique=True
    )

    # Controle de transmissão
    protocolo_envio: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    xml: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    recibo: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    data_envio: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    data_retorno: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    mensagem_erro: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
