from aiogram import Router
from bot.utils.menu import create_main_menu
from bot.log import logger
from aiogram.types import Message
from aiogram.filters import CommandStart  # Используем CommandStart для фильтрации команды "/start"
from bot.config import API_URL

import aiohttp

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    telegram_id = message.from_user.id
    logger.info(f"Получена команда '/start' от пользователя {telegram_id}")

    try:
        logger.info(f"Отправляем запрос на сервер для проверки наличия пользователя с ID {telegram_id}")

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_URL}/check_user", json={"telegram_id": telegram_id}) as resp:

                if resp.status == 200:
                    data = await resp.json()

                    if data['exists']:
                        try:
                            await message.answer(
                                "🎰 Добро пожаловать в казино! Ты уже зарегистрирован. Начни игру!",
                                reply_markup=create_main_menu()
                            )
                        except Exception as e:
                            logger.error(f"Ошибка при отправке меню: {e}")
                    else:
                        # Подставляем уникальную сумму и ник из ответа API
                        unique_amount = data.get("unique_amount")
                        minecraft_nick = data.get("minecraft_nick")

                        if unique_amount and minecraft_nick:
                            await message.answer(
                                f"❗ Ты не зарегистрирован. Для регистрации введи команду:\n"
                                f"/pay {minecraft_nick} {unique_amount}"
                            )
                        else:
                            # На всякий случай, если данных нет
                            await message.answer(
                                "❗ Ты не зарегистрирован. Для регистрации введи команду /pay {ник} {сумма}."
                            )
                else:
                    logger.error(f"Ошибка при запросе на сервер. Статус: {resp.status}")
    except Exception as e:
        logger.error(f"Ошибка при отправке запроса: {e}")

