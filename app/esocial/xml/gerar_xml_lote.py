
from sqlalchemy import or_

from app.database.local.models import EsocialDesligamento
from app.esocial.xml.desligamento import gerar_e_salvar_xml


def gerar_xml_em_lote(session, tamanho_lote=100):

    ultimo_id = 0

    total_processados = 0
    total_erros = 0

    while True:

        eventos = (
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.id > ultimo_id,
                EsocialDesligamento.id_evento.is_not(None),
                or_(
                    EsocialDesligamento.xml.is_(None),
                    EsocialDesligamento.xml == ""
                )
            )
            .order_by(EsocialDesligamento.id)
            .limit(tamanho_lote)
            .all()
        )

        if not eventos:
            break

        for evento in eventos:

            try:

                gerar_e_salvar_xml(evento, session)

                evento.mensagem_erro = None

                total_processados += 1

            except Exception as erro:

                evento.mensagem_erro = (
                    f"Erro na geração do XML: {str(erro)}"
                )

                total_erros += 1

                print(
                    f"Erro no evento {evento.id}: {erro}"
                )

            ultimo_id = evento.id

        try:

            session.commit()

        except Exception:

            session.rollback()
            raise

        print(
            f"Processados até o ID {ultimo_id}"
        )

    return {
        "processados": total_processados,
        "erros": total_erros
    }

if __name__ == "__main__":

    from app.database.local.connection import SessionLocal

    session = SessionLocal()

    try:

        resultado = gerar_xml_em_lote(session)

        print("\n===== RESULTADO =====")
        print(f"XMLs gerados: {resultado['processados']}")
        print(f"Erros: {resultado['erros']}")

    finally:
        session.close()