from app.database.local.connection import SessionLocal
from app.etl.transform.desligamento import tranformar_desligamento


session = SessionLocal()

try:
    eventos = tranformar_desligamento(session)
    session.add_all(eventos)
    session.commit()
    print(f'{len(eventos)} novos eventos gravados')

except Exception:
    session.rollback()
    raise

finally:
    session.close()