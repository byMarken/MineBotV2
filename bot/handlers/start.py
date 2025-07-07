from aiogram import Router
from bot.log import logger
from aiogram.types import Message
from aiogram.filters import CommandStart  # Используем CommandStart для фильтрации команды "/start"
from bot.config import API_URL
import aiohttp

router = Router()

@router.message(CommandStart())  # Исправляем на CommandStart
async def start_command(message: Message):
    telegram_id = message.from_user.id
    logger.info(f"Получена команда '/start' от пользователя {telegram_id}")

    try:
        # Логируем перед отправкой запроса
        logger.info(f"Отправляем запрос на сервер для проверки наличия пользователя с ID {telegram_id}")

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_URL}/check_user", json={"telegram_id": telegram_id}) as resp:

                # Логируем статус ответа
                logger.info(f"Ответ от сервера: {resp.status}")

                if resp.status == 200:
                    data = await resp.json()

                    # Логируем ответ от сервера
                    logger.info(f"Полученные данные: {data}")

                    if data['exists']:
                        # Пользователь существует
                        await message.answer("🎰 Добро пожаловать в казино! Ты уже зарегистрирован. Начни игру!")
                    else:
                        # Пользователь не найден, предлагаем регистрацию
                        await message.answer(
                            "❗ Ты не зарегистрирован. Введи команду: /pay {ник} {сумма} для регистрации.")
                else:
                    # Логируем ошибку, если статус не 200
                    logger.error(f"Ошибка при запросе на сервер. Статус: {resp.status}")
    except Exception as e:
        # Логируем исключения
        logger.error(f"Ошибка при отправке запроса: {e}")
