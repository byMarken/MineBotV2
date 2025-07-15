from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import Dict, Callable

from bot.keyboards.play_menu import create_play_menu
from bot.services.bet_manager import bet_manager  # Импортируем единственный экземпляр bet_manager

router = Router()

def create_bet_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="10$"), KeyboardButton(text="20$"), KeyboardButton(text="50$")],
            [KeyboardButton(text="100$"), KeyboardButton(text="200$"), KeyboardButton(text="500$")],
            [KeyboardButton(text="🔢 Ввести вручную")]
        ],
        resize_keyboard=True
    )

class CustomBetState(StatesGroup):
    waiting_for_bet = State()

# Хендлер: выбор ставки (открытие меню)
@router.message(F.text.startswith("💵 Ставка"))
async def choose_bet(message: types.Message):
    await message.answer(
        "💰 Выберите новую ставку:",
        reply_markup=create_bet_menu()
    )

# Хендлер: выбор фиксированной ставки
@router.message(F.text.in_(["10$", "20$", "50$", "100$", "200$", "500$"]))
async def set_bet(message: types.Message):
    user_id = message.from_user.id
    new_bet = int(message.text.replace("$", ""))
    bet_manager.set_bet(user_id, new_bet)
    await message.answer(
        f"✅ Ставка установлена: {new_bet}$",
        reply_markup=create_play_menu(user_id)  # возвращаем меню слотов
    )

# Хендлер: ручной ввод
@router.message(F.text == "🔢 Ввести вручную")
async def ask_custom_bet(message: types.Message, state: FSMContext):
    await state.set_state(CustomBetState.waiting_for_bet)
    await message.answer("✍️ Введите сумму ставки:", reply_markup=create_bet_menu())

# Хендлер: установка вручную введённой ставки
@router.message(CustomBetState.waiting_for_bet)
async def set_custom_bet(message: types.Message, state: FSMContext):
    try:
        bet = int(message.text)  # тут не должно быть "$"
        if bet <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введите корректное целое число больше 0.")
        return

    user_id = message.from_user.id
    bet_manager.set_bet(user_id, bet)

    await message.answer(
        f"✅ Ставка установлена: {bet}$",
        reply_markup=create_play_menu(user_id)  # возвращаем меню
    )

    await state.clear()
