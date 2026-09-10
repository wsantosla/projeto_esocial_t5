from app.database.local.connection import SessionLocal
from app.database.local.models import EsocialDesligamento
from app.esocial.validators.desligamento import validar_desligamento


session = SessionLocal()

try:

    eventos=(
        session.query(EsocialDesligamento).all()
    )

    for evento in eventos:
        erros = validar_desligamento(evento)

        if erros:
            print(f'Matricula{evento.matricula}')

            for erro in erros:
                print(f'-{erro}')

        else:
            print(f'Matricula{evento.matricula} ok')
finally:
    session.close()