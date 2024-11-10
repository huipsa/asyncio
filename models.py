from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from database import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


class Person(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(20))
    eye_color = Column(String(50))
    films = Column(String(600))
    gender = Column(String(100))
    hair_color = Column(String(50))
    height = Column(String(50))
    homeworld = Column(String(200))
    mass = Column(String(50))
    name = Column(String(200))
    skin_color = Column(String(50))
    species = Column(String(600))
    starships = Column(String(600))
    vehicles = Column(String(600))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
