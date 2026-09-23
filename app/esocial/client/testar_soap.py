from app.database.local.connection import SessionLocal
from app.database.local.models import EsocialDesligamento
from app.esocial.client.lote import gerar_lote_eventos
from app.esocial.client.soap import criar_envelope_soap


def testar_soap():
    session = SessionLocal()

    try:

        evento=(
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.xml.is_not(None),
                EsocialDesligamento.id_evento.is_not(None),
            )
            .first()
        )

        if not evento:
            print("Nenhum evento encontrado")
            return
        print("Matricula:", evento.matricula)
        print("Id do evento:",evento.id_evento)

        #1.Gera o Lote
        lote = gerar_lote_eventos(evento)

        #2.Gera o envelope SOAP
        soap=criar_envelope_soap(lote)

        print("\n======SOAP======\n")

        print(soap.decode("UTF-8"))

    finally:
        session.close()
if __name__ == "__main__":
    testar_soap()