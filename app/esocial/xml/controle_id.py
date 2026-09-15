from datetime import datetime
from sqlalchemy import select
from app.config.esocial import ESOCIAL_TP_INSC,ESOCIAL_NR_INSC
from app.database.local.connection import SessionLocal
from app.database.local.models import EsocialControleId

def obter_sequencial(agora:datetime):


    with SessionLocal() as session:

        registro =session.scalar(
        select(EsocialControleId).where(
            EsocialControleId.tp_insc == ESOCIAL_TP_INSC,
            EsocialControleId.nr_insc == ESOCIAL_NR_INSC,
            EsocialControleId.data_hora == agora
        )
    )    
    if registro:
        registro.sequencial += 1
        sequencial = registro.sequencial
    else:
        registro = EsocialControleId(tp_insc=ESOCIAL_TP_INSC,
                                     nr_insc=ESOCIAL_NR_INSC,
                                     data_hora=agora,
                                     sequencial=1)
        
        session.add(registro)
        sequencial = 1
    session.commit()
    return sequencial

        