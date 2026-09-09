from app.database.local.models import EsocialDesligamento

def validar_desligamento(evento):

    erros = []

    if not evento.matricula:
        erros.append('Matricula não informada.')
    if not evento.cpf_trab:
        erros.append('Cpf nao informado.')
    if len(evento.cpf_trab) != 11:
        erros.append('CPF deve possuir 11 Digitos')
    if not evento.dt_deslig:
        erros.append('data não informada')
    if not evento.mtv_deslig:
        erros.append('Motivo de desligamento não informado')
    if len(evento.mtv_deslig) != 2:
        erros.append('Motivo de desligamto deve possuir 2 caracteres')
    return erros