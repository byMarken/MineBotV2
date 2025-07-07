from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from db.models import Base
from dotenv import load_dotenv
import os

# Загрузить переменные из .env
load_dotenv()

# Получить URL из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Создание движка и сессии
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Инициализация базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
