from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound
from db.models import User, PendingAuthorization
from db.database import SessionLocal
from server.utils.services import PendingService, UserService, DepositService  # Импортируем наш сервис
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

class PaymentRequest(BaseModel):
    sender: str
    amount: float  # float, потому что парсер присылает float

@router.post("/dep")
async def dep(data: PaymentRequest):
    async with SessionLocal() as session:
        pending_service = PendingService(session)
        user_service = UserService(session)
        deposit_service = DepositService(session)

        # Ищем запись по уникальной сумме
        pending = await pending_service.get_pending_by_unique_amount(data.amount)

        if not pending:
            # Если нет в pending — это пополнение баланса
            deposit = await deposit_service.increase_balance_parser(data.sender, data.amount)
            return {"status": "success", "message": f"Баланс {data.sender} пополнен!"}

        # Проверка: существует ли уже пользователь с таким ником
        existing_user = await user_service.get_user_by_minecraft_nick(data.sender)
        if existing_user:
            await pending_service.delete_pending(pending.telegram_id)
            return {"status": "error", "message": f"Пользователь с ником '{data.sender}' уже существует. Регистрация сброшена"}

        # Обновляем pending запись с ником
        pending = await pending_service.update_pending_with_nickname(pending.telegram_id, data.sender)

        # Переносим в users
        new_user = await user_service.create_user(pending.telegram_id, pending.minecraft_nick)

        # Удаляем запись из pending
        await pending_service.delete_pending(pending.telegram_id)

        return {"status": "success", "message": f"Пользователь {data.sender} зарегистрирован!"}


