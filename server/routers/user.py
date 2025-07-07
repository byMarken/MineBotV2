from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import select
from db.models import User, PendingAuthorization
from db.database import SessionLocal
from ..utils.unique_amount import generate_unique_amount  # твоя функция генерации уникальной суммы

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
    unique_amount: Optional[int] = None  # Добавим для pending
    message: Optional[str] = None        # Например, для подсказки регистрации


# ✅ Проверка — существует ли пользователь
@router.post("/check_user", response_model=UserCheckResponse)
async def check_user(request: UserCheckRequest):
    async with SessionLocal() as session:
        # Проверяем пользователя
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

        # Пользователя нет — проверяем в pending
        stmt_pending = select(PendingAuthorization).where(PendingAuthorization.telegram_id == request.telegram_id)
        result_pending = await session.execute(stmt_pending)
        pending = result_pending.scalar_one_or_none()

        # Если запись есть — удаляем её
        if pending:
            await session.delete(pending)
            await session.commit()  # Подтверждаем удаление

        # Генерируем новую уникальную сумму для пополнения
        unique_sum = await generate_unique_amount(session)

        # Создаём новую запись в pending_authorizations
        new_pending = PendingAuthorization(
            telegram_id=request.telegram_id,
            unique_amount=unique_sum
        )
        session.add(new_pending)
        await session.commit()
        await session.refresh(new_pending)

        # Возвращаем данные для регистрации с новой уникальной суммой
        return UserCheckResponse(
            exists=False,
            unique_amount=unique_sum,
            message="Пользователь не зарегистрирован. Пожалуйста, пополните баланс на уникальную сумму для авторизации.",
            minecraft_nick=f"hoems743"  # пока статичный ник
        )

