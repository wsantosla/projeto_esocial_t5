from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


engine_local = create_engine



load_dotenv()

DB_HOST=os.getenv("LOCAL_DB_HOST")
DB_PORT=os.getenv("LOCAL_DB_PORT")
DB_NAME=os.getenv("LOCAL_DB_NAME")
DB_USER=os.getenv("LOCAL_DB_USER")
DB_PASSWORD=os.getenv("LOCAL_DB_PASSWORD")
DATABASE_URL=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine_local = create_engine(DATABASE_URL,pool_pre_ping=True)

SessionLocal = sessionmaker(
    bind=engine_local,
    autoflush=False,
    autocommit=False
    )