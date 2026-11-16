
from app.database.local.connection import SessionLocal
from app.database.local.models import EsocialDesligamento

from app.esocial.client.lote import gerar_lote_eventos
from app.esocial.client.soap import criar_envelope_soap
from app.esocial.client.enviar import enviar_soap

from app.esocial.client.validar_lote import validar_lote


def testar_envio():

    with SessionLocal() as session:

        evento = (
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.xml.is_not(None),
                EsocialDesligamento.id_evento.is_not(None),
                EsocialDesligamento.status == "PENDENTE",
                EsocialDesligamento.protocolo_envio.is_(None),
            )
            .order_by(EsocialDesligamento.id.asc())
            .first()
        )

        if not evento:
            print("Nenhum desligamento pendente encontrado.")
            return

        print("\n===================================")
        print("DESLIGAMENTO SELECIONADO")
        print("===================================")
        print("Matrícula:", evento.matricula)
        print("ID evento:", evento.id_evento)
        print("Status:", evento.status)

        # Gera lote do grupo 2 - S-2299
        lote = gerar_lote_eventos(
            xml=evento.xml,
            id_evento=evento.id_evento,
            grupo="2"
        )

        # Valida estrutura do lote
        validar_lote(
            lote,
            grupo_esperado="2"
        )

        print("\nLote validado.")

        # Gera envelope SOAP
        soap = criar_envelope_soap(lote)

        print("Envelope SOAP preparado.")

        # Envia para o eSocial
        resposta = enviar_soap(
            soap_xml=soap,
            id_evento=evento.id_evento
        )

        print("\nEnvio concluído.")
        print("HTTP:", resposta.status_code)


if __name__ == "__main__":
    testar_envio()
