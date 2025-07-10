from aiogram import Router, types, F

from bot.utils.service import BetManager

router = Router()

# Инициализация объекта ставки
bet_manager = BetManager()

@router.message(F.text == "Размер ставки 💎")
async def choose_bet(message: types.Message):
    await message.answer(
        text="Выберите размер ставки:",
        reply_markup=bet_manager.get_keyboard()
    )

@router.callback_query(F.data == "increase_bet")
async def increase_bet(callback: types.CallbackQuery):
    bet_manager.increase()
    await callback.message.edit_reply_markup(
        reply_markup=bet_manager.get_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "decrease_bet")
async def decrease_bet(callback: types.CallbackQuery):
    bet_manager.decrease()
    await callback.message.edit_reply_markup(
        reply_markup=bet_manager.get_keyboard()
    )
    await callback.answer()
