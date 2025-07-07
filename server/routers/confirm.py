from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select, delete
from db.models import PendingAuthorization, User
from db.database import SessionLocal
from sqlalchemy.exc import NoResultFound

router = APIRouter()

class PaymentConfirmationRequest(BaseModel):
    sender: str
    amount: float  # float потому что парсер присылает float

@router.post("/confirm_payment")
async def confirm_payment(data: PaymentConfirmationRequest):
    async with SessionLocal() as session:
        # Ищем запись по сумме
        stmt = select(PendingAuthorization).where(PendingAuthorization.unique_amount == int(data.amount))
        result = await session.execute(stmt)
        pending = result.scalar_one_or_none()

        if not pending:
            return {"status": "error", "message": "Не найдена подходящая сумма"}

        # Обновляем pending запись с ником
        pending.minecraft_nick = data.sender
        await session.commit()

        # Переносим в users
        new_user = User(
            telegram_id=pending.telegram_id,
            minecraft_nick=pending.minecraft_nick,
            balance=0,
            fake_balance=0
        )
        session.add(new_user)

        # Удаляем из pending
        await session.delete(pending)
        await session.commit()

        return {"status": "success", "message": f"Пользователь {data.sender} зарегистрирован!"}
