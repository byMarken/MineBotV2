from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from server.utils.services import UserService, PendingService
from db.database import SessionLocal

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
        user_service = UserService(session)
        pending_service = PendingService(session)

        # Проверяем пользователя в таблице User
        user = await user_service.get_user_by_telegram_id(request.telegram_id)
        if user:
            return UserCheckResponse(
                exists=True,
                telegram_id=user.telegram_id,
                minecraft_nick=user.minecraft_nick,
                balance=user.balance,
                fake_balance=user.fake_balance
            )

        # Пользователя нет — проверяем в Pending
        pending = await pending_service.get_pending_by_telegram_id(request.telegram_id)

        # Если запись есть в pending, удаляем её
        if pending:
            await pending_service.delete_pending(request.telegram_id)

        # Генерируем новую уникальную сумму для пополнения
        unique_sum = await pending_service.create_pending(request.telegram_id)

        # Возвращаем данные для регистрации с новой уникальной суммой
        return UserCheckResponse(
            exists=False,
            unique_amount=unique_sum.unique_amount,
            message="Пользователь не зарегистрирован. Пожалуйста, пополните баланс на уникальную сумму для авторизации.",
            minecraft_nick=f"gnrfugdnfs"  # Пока статичный ник
        )
