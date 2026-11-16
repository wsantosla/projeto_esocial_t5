
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.config.esocial import (
    ESOCIAL_TP_INSC,
    ESOCIAL_NR_INSC
)

from app.database.local.connection import SessionLocal
from app.database.local.models import EsocialControleId


def obter_sequencial(agora: datetime):

    with SessionLocal() as session:

        tabela = EsocialControleId.__table__

        comando = (
            insert(tabela)
            .values(
                tp_insc=ESOCIAL_TP_INSC,
                nr_insc=ESOCIAL_NR_INSC,
                data_hora=agora,
                sequencial=1
            )
            .on_conflict_do_update(
                constraint="uq_esocial_controle_id",
                set_={
                    "sequencial": tabela.c.sequencial + 1
                }
            )
            .returning(tabela.c.sequencial)
        )

        sequencial = session.execute(comando).scalar_one()

        session.commit()

        return sequencial
