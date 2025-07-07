from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import select
from db.models import User
from db.database import SessionLocal  # это твой async_sessionmaker

router = APIRouter()


# Модели запросов и ответов
class UserCheckRequest(BaseModel):
    telegram_id: int

class UserCheckResponse(BaseModel):
    exists: bool
    telegram_id: Optional[int] = None
    minecraft_nick: Optional[str] = None
    balance: Optional[int] = None
    fake_balance: Optional[int] = None

class UserResponse(BaseModel):
    telegram_id: int
    minecraft_nick: str
    balance: int
    fake_balance: int


# ✅ Проверка — существует ли пользователь
@router.post("/check_user", response_model=UserCheckResponse)
async def check_user(request: UserCheckRequest):
    async with SessionLocal() as session:
        stmt = select(User).where(User.telegram_id == request.telegram_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            return UserCheckResponse(
                exists=True,
                telegram_id=user.telegram_id,
                minecraft_nick=user.minecraft_nick,
                balance=user.balance,
                fake_balance=user.fake_balance
            )

        return UserCheckResponse(exists=False)


# ✅ Регистрация нового пользователя
@router.post("/register", response_model=UserResponse)
async def register_user(request: UserCheckRequest):
    async with SessionLocal() as session:
        stmt = select(User).where(User.telegram_id == request.telegram_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            return user

        # Создаём нового пользователя
        new_user = User(
            telegram_id=request.telegram_id,
            minecraft_nick=f"user{request.telegram_id}",
            balance=0,
            fake_balance=0
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user
