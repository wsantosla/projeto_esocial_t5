from app.database.local.connection import SessionLocal
from app.database.local.models import EsocialDesligamento

from app.esocial.client.lote import gerar_lote_eventos
from app.esocial.client.validar_lote import validar_lote


def testar_lote():

    session = SessionLocal()

    try:

        evento = (
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.xml.is_not(None),
                EsocialDesligamento.id_evento.is_not(None),
            )
            .first()
        )

        if not evento:
            print(
                "Nenhum evento assinado encontrado."
            )
            return

        lote = gerar_lote_eventos(evento)

        validar_lote(lote)

        print("\n===== LOTE =====\n")
        print(
            lote.decode("UTF-8")
        )

    finally:
        session.close()


if __name__ == "__main__":
    testar_lote()