import random
from sqlalchemy import select
from db.models import PendingAuthorization

async def generate_unique_amount(session) -> int:
    for _ in range(10):
        candidate = random.randint(1, 100)  # от 1 до 100
        stmt = select(PendingAuthorization).where(PendingAuthorization.unique_amount == candidate)
        result = await session.execute(stmt)
        exists = result.scalar_one_or_none()
        if not exists:
            return candidate

    max_stmt = select(PendingAuthorization.unique_amount).order_by(PendingAuthorization.unique_amount.desc())
    max_result = await session.execute(max_stmt)
    max_val = max_result.scalar_one()
    return max_val + 1 if max_val else 1
