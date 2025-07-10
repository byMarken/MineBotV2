import asyncio
from aiogram import Router, F, types
from aiogram.enums.dice_emoji import DiceEmoji
from functools import lru_cache
from typing import List

router = Router()

# Список символов Telegram Dice по индексам 0–3
SYMBOLS = ["BAR", "🍇", "🍋", "7️⃣"]  # Индексы: 0, 1, 2, 3


@lru_cache(maxsize=64)
def get_combo_parts(dice_value: int) -> List[str]:
    """
    Возвращает комбинацию из 3 символов по значению Telegram Dice (в порядке left → center → right).
    """
    dice_value -= 1  # Приводим к диапазону 0–63
    result = []

    for _ in range(3):
        result.append(SYMBOLS[dice_value % 4])
        dice_value //= 4

    return result


@lru_cache(maxsize=64)
def get_combo_text(dice_value: int, l10n=None) -> str:
    """
    Возвращает строку "символ | символ | символ" по значению кубика.
    """
    parts = get_combo_parts(dice_value)
    if l10n:
        parts = [l10n.format_value(p) for p in parts]
    return " | ".join(parts)


@lru_cache(maxsize=64)
def get_score_change(dice_value: int) -> int:
    """
    Возвращает множитель выигрыша (0, 5, 7, 10) по комбинации символов.
    """
    dice_value -= 1
    first = dice_value % 4
    second = (dice_value // 4) % 4
    third = (dice_value // 16) % 4

    if first == second == third == 3:
        return 10  # 🎉 Три семерки
    elif (first == second == 3) or (second == third == 3) or (first == third == 3):
        return 5  # Две семёрки
    elif first == second == third:
        return 7  # Три одинаковых
    else:
        return 0


@router.message(F.text == "🎰 Крутить слоты")
async def slot_spin(message: types.Message):
    # Отправляем слотовый кубик (с анимацией)
    dice_msg = await message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)

    # Ждём окончания анимации (примерно 4 секунды)
    await asyncio.sleep(3)

    value = dice_msg.dice.value
    combo = get_combo_text(value)
    multiplier = get_score_change(value)
    bet = 10
    win = bet * multiplier

    await message.answer(
        f"🎰 Ваша комбинация: {combo}\n"
        f"Ваша ставка: {bet}$\n"
        f"Выигрыш: {win}$"
    )
