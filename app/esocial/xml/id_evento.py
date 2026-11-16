from datetime import datetime
from app.config.esocial import ESOCIAL_TP_INSC,ESOCIAL_NR_INSC
from app.esocial.xml.controle_id import obter_sequencial

def gerar_id_evento():

    nr_incricao=ESOCIAL_NR_INSC.ljust(14,"0")
    agora =datetime.now().replace(microsecond=0)
    sequencial=obter_sequencial(agora)
    id_evento = ("ID"
                 +ESOCIAL_TP_INSC
                 +nr_incricao+agora.strftime("%Y%m%d%H%M%S")
                 +f"{sequencial:05d}"
    )
    if len(id_evento) != 36:
        raise ValueError(f"Id do invalido:{id_evento}" 
                          f"possui {len(id_evento)}")

    return id_evento


def atribuir_id_evento(evento):

    if evento.id_evento:
        return evento.id_evento

    id_evento = gerar_id_evento()

    evento.id_evento = id_evento

    return id_evento
    
    



if __name__ == "__main__":

    from sqlalchemy import select

    from app.database.local.connection import SessionLocal
    from app.database.local.models import EsocialDesligamento

    with SessionLocal() as session:

        eventos = session.scalars(
            select(EsocialDesligamento).where(
                EsocialDesligamento.tipo_evento == "S-2299",
                EsocialDesligamento.status == "PENDENTE",
                EsocialDesligamento.id_evento.is_(None)
            )
        ).all()

        print(f"Eventos encontrados: {len(eventos)}")

        for evento in eventos:
            id_evento = atribuir_id_evento(evento)

            print(
                f"Matrícula: {evento.matricula} | "
                f"ID: {id_evento}"
            )

        session.commit()

        print("\nIDs atribuídos e salvos com sucesso!")
