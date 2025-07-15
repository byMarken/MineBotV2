from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


router = Router()

@router.message(F.text == "Выбор игрового режима 🎮")
async def show_game_modes(message: types.Message):
    await message.answer(
        "🎮 Выберите режим игры:",
        reply_markup=create_slots_menu()
    )
def create_slots_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎰 Крутить слоты")],
            [KeyboardButton(text="⬅️ Назад в меню")]
        ],
        resize_keyboard=True
    )

