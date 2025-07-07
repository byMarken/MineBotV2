from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from db.models import User, PendingAuthorization
from ..utils.unique_amount import generate_unique_amount  # твоя функция генерации уникальной суммы


# Сервис для работы с пользователями
class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        """Получить пользователя по telegram_id."""
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, telegram_id: int, minecraft_nick: str) -> User:
        """Создать нового пользователя в таблице User."""
        new_user = User(
            telegram_id=telegram_id,
            minecraft_nick=minecraft_nick,
            balance=0,
            fake_balance=0
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user


# Сервис для работы с таблицей PendingAuthorization
class PendingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_pending_by_unique_amount(self, unique_amount: float) -> PendingAuthorization | None:
        """Получить запись из таблицы pending по уникальной сумме."""
        stmt = select(PendingAuthorization).where(
        PendingAuthorization.unique_amount == int(unique_amount))  # Преобразуем в int, если это необходимо
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_pending_by_telegram_id(self, telegram_id: int) -> PendingAuthorization | None:
        """Получить запись из таблицы pending по telegram_id."""
        stmt = select(PendingAuthorization).where(PendingAuthorization.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_pending(self, telegram_id: int) -> PendingAuthorization:
        """Создать запись в таблице pending для авторизации."""
        unique_amount = await generate_unique_amount(self.session)
        new_pending = PendingAuthorization(
            telegram_id=telegram_id,
            unique_amount=unique_amount
        )
        self.session.add(new_pending)
        await self.session.commit()
        await self.session.refresh(new_pending)
        return new_pending

    async def update_pending_with_nickname(self, telegram_id: int, nickname: str) -> PendingAuthorization:
        """Обновить запись в pending с ником игрока."""
        stmt = select(PendingAuthorization).where(PendingAuthorization.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        pending = result.scalar_one_or_none()

        if pending:
            pending.minecraft_nick = nickname
            await self.session.commit()
            await self.session.refresh(pending)
            return pending
        else:
            raise NoResultFound("Pending record not found.")

    async def delete_pending(self, telegram_id: int) -> None:
        """Удалить запись из таблицы pending."""
        stmt = select(PendingAuthorization).where(PendingAuthorization.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        pending = result.scalar_one_or_none()

        if pending:
            await self.session.delete(pending)
            await self.session.commit()
