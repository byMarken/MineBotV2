from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound
from db.models import User, PendingAuthorization
from db.database import SessionLocal
from server.utils.services import PendingService, UserService  # Импортируем наш сервис
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

class PaymentConfirmationRequest(BaseModel):
    sender: str
    amount: float  # float, потому что парсер присылает float

@router.post("/confirm_payment")
async def confirm_payment(data: PaymentConfirmationRequest):
    async with SessionLocal() as session:
        pending_service = PendingService(session)
        user_service = UserService(session)

        # Ищем запись по уникальной сумме
        pending = await pending_service.get_pending_by_unique_amount(data.amount)

        if not pending:
            return {"status": "error", "message": "Не найдена подходящая сумма"}

        # Обновляем pending запись с ником
        pending = await pending_service.update_pending_with_nickname(pending.telegram_id, data.sender)

        # Переносим в users
        new_user = await user_service.create_user(pending.telegram_id, pending.minecraft_nick)

        # Удаляем запись из pending
        await pending_service.delete_pending(pending.telegram_id)

        return {"status": "success", "message": f"Пользователь {data.sender} зарегистрирован!"}
