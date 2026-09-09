from app.database.local.models import StgDesligamento, EsocialDesligamento

def tranformar_desligamento(session):

    registros=(
        session.query(StgDesligamento).all()
    )
    eventos= []
    for registro in registros:

        evento_existente= (
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.matricula == registro.matricula
            )
            .first()
        )
        if evento_existente:
            continue
 
        evento = EsocialDesligamento(
            matricula=registro.matricula,
            cpf_trab=registro.cpf,
            dt_deslig=registro.data_afastamento,
            mtv_deslig=registro.codigo_esocial,
        )

        eventos.append(evento)

    return eventos