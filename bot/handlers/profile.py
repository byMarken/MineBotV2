from aiogram import Router, F, types
from bot.config import API_URL  # Убедись, что API_URL типа http://localhost:8000 или где твой сервер
import aiohttp
from bot.log import logger
from bot.utils.service import beautiful_balance

router = Router()

@router.message(F.text == "Профиль 👤")
async def profile(message: types.Message):
    telegram_id = message.from_user.id
    logger.info(f"Запрошен профиль пользователем {telegram_id}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_URL}/get_user", json={"telegram_id": telegram_id}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    text = (
                        f"👤 Профиль:\n"
                        f"• Ник в Minecraft: {data['minecraft_nick']}\n"
                        f"• Баланс: {beautiful_balance(data['balance'])} 💰"
                    )
                elif resp.status == 404:
                    text = "❗ Профиль не найден. Похоже, вы не зарегистрированы."
                else:
                    text = "⚠️ Ошибка при получении профиля. Попробуйте позже."
    except Exception as e:
        logger.error(f"Ошибка при запросе профиля: {e}")
        text = "❗ Произошла ошибка при подключении к серверу."

    await message.answer(text)
