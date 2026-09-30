from datetime import datetime

from lxml import etree

from app.database.local.connection import SessionLocal
from app.database.local.models import EsocialDesligamento


NS = {
    "evt": (
        "http://www.esocial.gov.br/"
        "schema/evt/retornoEvento/v1_3_0"
    )
}


def processar_retorno_consulta(xml_resposta):

    if isinstance(xml_resposta, str):
        xml_resposta = xml_resposta.encode("utf-8")

    root = etree.fromstring(xml_resposta)

    retorno_evento = root.find(
        ".//evt:retornoEvento",
        namespaces=NS
    )

    if retorno_evento is None:
        raise ValueError(
            "Bloco retornoEvento não encontrado."
        )

    id_evento = retorno_evento.get("Id")

    if not id_evento:
        raise ValueError(
            "Id do evento não encontrado."
        )

    processamento = retorno_evento.find(
        "evt:processamento",
        namespaces=NS
    )

    if processamento is None:
        raise ValueError(
            "Bloco processamento não encontrado."
        )

    cd_resposta = processamento.findtext(
        "evt:cdResposta",
        namespaces=NS
    )

    desc_resposta = processamento.findtext(
        "evt:descResposta",
        namespaces=NS
    )

    # ==========================================================
    # OCORRÊNCIA
    # ==========================================================

    ocorrencia = processamento.find(
        "evt:ocorrencias/evt:ocorrencia",
        namespaces=NS
    )

    codigo = None
    descricao = None
    localizacao = None

    if ocorrencia is not None:

        codigo = ocorrencia.findtext(
            "evt:codigo",
            namespaces=NS
        )

        descricao = ocorrencia.findtext(
            "evt:descricao",
            namespaces=NS
        )

        localizacao = ocorrencia.findtext(
            "evt:localizacao",
            namespaces=NS
        )

    # ==========================================================
    # RECIBO
    # ==========================================================

    recibo = retorno_evento.findtext(
        ".//evt:nrRecibo",
        namespaces=NS
    )

    # ==========================================================
    # BANCO
    # ==========================================================

    with SessionLocal() as session:

        evento = (
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.id_evento == id_evento
            )
            .first()
        )

        if evento is None:
            raise ValueError(
                f"Evento não encontrado no banco: {id_evento}"
            )

        evento.data_retorno = datetime.now()

        # ======================================================
        # EVENTO PROCESSADO
        # ======================================================

        if cd_resposta == "201":

            evento.status = "PROCESSADO"
            evento.mensagem_erro = None

            # Salva o recibo somente se ele existir
            if recibo:
                evento.recibo = recibo

        # ======================================================
        # EVENTO REJEITADO
        # ======================================================

        else:

            evento.status = "REJEITADO"

            mensagem = []

            if cd_resposta:
                mensagem.append(
                    f"Código resposta: {cd_resposta}"
                )

            if desc_resposta:
                mensagem.append(
                    f"Resposta: {desc_resposta}"
                )

            if codigo:
                mensagem.append(
                    f"Código ocorrência: {codigo}"
                )

            if descricao:
                mensagem.append(
                    f"Ocorrência: {descricao}"
                )

            if localizacao:
                mensagem.append(
                    f"Localização: {localizacao}"
                )

            evento.mensagem_erro = "\n".join(mensagem)

        session.commit()

        # ======================================================
        # RESULTADO
        # ======================================================

        print("\n========== RESULTADO ==========")

        print(f"ID evento: {id_evento}")
        print(f"Código resposta: {cd_resposta}")
        print(f"Descrição: {desc_resposta}")

        if recibo:
            print(f"Recibo: {recibo}")

        if codigo:
            print(f"Código ocorrência: {codigo}")

        if descricao:
            print(f"Ocorrência: {descricao}")

        if localizacao:
            print(f"Localização: {localizacao}")

        print(f"Status: {evento.status}")

        if evento.mensagem_erro:
            print("\nMensagem registrada:")
            print(evento.mensagem_erro)

        print("================================")

        return evento

