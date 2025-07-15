import asyncio
from aiogram import Router, F, types
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from functools import lru_cache
from typing import List

from bot.handlers.select_game import create_slots_menu
from bot.keyboards.play_menu import create_play_menu
from bot.services.bet_manager import bet_manager  # Импортируем bet_manager

router = Router()

SYMBOLS = ["BAR", "🍇", "🍋", "7️⃣"]

@lru_cache(maxsize=64)
def get_combo_parts(dice_value: int) -> List[str]:
    dice_value -= 1
    result = []
    for _ in range(3):
        result.append(SYMBOLS[dice_value % 4])
        dice_value //= 4
    return result

@lru_cache(maxsize=64)
def get_combo_text(dice_value: int, l10n=None) -> str:
    parts = get_combo_parts(dice_value)
    if l10n:
        parts = [l10n.format_value(p) for p in parts]
    return " | ".join(parts)

@lru_cache(maxsize=64)
def get_score_change(dice_value: int) -> int:
    dice_value -= 1
    first = dice_value % 4
    second = (dice_value // 4) % 4
    third = (dice_value // 16) % 4

    if first == second == third == 3:
        return 10
    elif (first == second == 3) or (second == third == 3) or (first == third == 3):
        return 5
    elif first == second == third:
        return 7
    else:
        return 0

@router.message(F.text == "🎰 Крутить слоты")
async def show_slot_interface(message: types.Message):
    user_id = message.from_user.id
    # при первом входе просто не надо ничего делать — ставка по умолчанию уже есть в bet_manager
    await message.answer(
        "🎰 Вы вошли в режим слотов.\nНажмите 🕹️ Играть, чтобы начать!",
        reply_markup=create_play_menu(user_id)
    )

@router.message(F.text == "🕹️ Играть")
async def slot_spin(message: types.Message):
    user_id = message.from_user.id
    bet = bet_manager.get_bet(user_id)  # Ставка будет теперь из bet_manager

    dice_msg = await message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
    await asyncio.sleep(2.5)

    value = dice_msg.dice.value
    combo = get_combo_text(value)
    multiplier = get_score_change(value)
    win = bet * multiplier

    await message.answer(
        f"🎰 Ваша комбинация: {combo}\n"
        f"Ваша ставка: {bet}$\n"
        f"Выигрыш: {win}$"
    )

@router.message(F.text == "📕 Правила")
async def show_rules(message: types.Message):
    await message.answer(
        "📜 *Правила игры в слоты:*\n\n"
        "🎰 В казино доступно 4 элемента:\n"
        "• BAR\n"
        "• 🍇 Виноград\n"
        "• 🍋 Лимон\n"
        "• 7️⃣ Семь\n\n"
        "🔢 Всего комбинаций: 64\n\n"
        "💥 *Выигрышные комбинации:*\n"
        "• 7️⃣7️⃣7️⃣ — ставка ×10\n"
        "• 7️⃣7️⃣ + любой символ — ставка ×5\n"
        "• 3 одинаковых символа — ставка ×7\n\n"
        "💸 Если нет совпадений — выигрыш 0",
        parse_mode="Markdown"
    )

@router.message(F.text == "⬅️ Назад в режимы")
async def back_to_modes(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🔙 Вы вернулись в выбор режима.",
        reply_markup=create_slots_menu()
    )
