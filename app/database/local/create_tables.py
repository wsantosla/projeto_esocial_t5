from app.database.local.connection import engine_local
from app.database.local.models import Base


print("Banco:", engine_local.url)

print("Tabelas que o SQLAlchemy conhece:")
print(Base.metadata.tables.keys())

Base.metadata.create_all(
    bind=engine_local
)

print("Processo finalizado!")