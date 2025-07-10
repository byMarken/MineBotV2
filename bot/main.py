import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from bot.config import BOT_TOKEN
from bot.handlers import start, profile, bet_size, select_game, slot_machine, back
from bot.utils import menu
from loguru import logger

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(bet_size.router)
    dp.include_router(select_game.router)
    dp.include_router(profile.router)
    dp.include_router(slot_machine.router)
    dp.include_router(back.router)

    logger.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


