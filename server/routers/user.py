from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

# Модели запросов и ответов
class UserCheckRequest(BaseModel):
    telegram_id: int

class UserResponse(BaseModel):
    telegram_id: int
    username: str
    first_name: str

# Список для имитации проверки (без сохранения)
existing_users = {
    7823560771: {"telegram_id": 7823560771, "username": "user123", "first_name": "John"},
    67890: {"telegram_id": 67890, "username": "user678", "first_name": "Jane"}
}
class UserCheckResponse(BaseModel):
    exists: bool
    telegram_id: int | None = None
    username: str | None = None
    first_name: str | None = None

# Обновите эндпоинт
@router.post("/check_user", response_model=UserCheckResponse)  # Используем новую модель
async def check_user(request: UserCheckRequest):
    user = existing_users.get(request.telegram_id)
    if user:
        return {
            "exists": True,
            "telegram_id": user["telegram_id"],
            "username": user["username"],
            "first_name": user["first_name"]
        }
    return {"exists": False}


# Регистрация пользователя (пока не сохраняем, просто возвращаем данные)
@router.post("/register", response_model=UserResponse)
async def register_user(request: UserCheckRequest):
    if request.telegram_id not in existing_users:
        # Возвращаем фейковые данные для регистрации
        return {"telegram_id": request.telegram_id, "username": f"user{request.telegram_id}", "first_name": f"User{request.telegram_id}"}
    return {"telegram_id": request.telegram_id, "username": existing_users[request.telegram_id]["username"], "first_name": existing_users[request.telegram_id]["first_name"]}