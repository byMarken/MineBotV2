from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.database import SessionLocal
from server.utils.services import UserService

router = APIRouter()


class UserProfileRequest(BaseModel):
    telegram_id: int


class UserProfileResponse(BaseModel):
    minecraft_nick: str
    balance: int


@router.post("/get_user", response_model=UserProfileResponse)
async def get_user_profile(request: UserProfileRequest):
    async with SessionLocal() as session:
        user_service = UserService(session)
        result = await user_service.get_nick_and_balance_by_telegram_id(request.telegram_id)

        if result:
            nick, balance = result
            return UserProfileResponse(minecraft_nick=nick, balance=balance)
        else:
            raise HTTPException(status_code=404, detail="User not found")
