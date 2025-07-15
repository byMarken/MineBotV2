from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router

router = Router()

def create_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Пополнить 💸"), KeyboardButton(text="Вывести 💰")],
            [KeyboardButton(text="Выбор игрового режима 🎮")],
            [KeyboardButton(text="Профиль 👤"), KeyboardButton(text="О нас")]
        ],
        resize_keyboard=True,
    )

