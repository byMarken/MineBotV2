from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router, F, types

from bot.utils.menu import create_main_menu

router = Router()

@router.message(F.text == "⬅️ Назад в меню")
async def back_to_main_menu(message: types.Message):
    await message.answer("Главное меню:", reply_markup=create_main_menu())