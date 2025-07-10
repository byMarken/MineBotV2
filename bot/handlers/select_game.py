from aiogram import Router, types, F

from bot.utils.service import create_slots_menu

router = Router()

@router.message(F.text == "Выбор игрового режима 🎮")
async def show_game_modes(message: types.Message):
    await message.answer(
        "🎮 Выберите режим игры:",
        reply_markup=create_slots_menu()
    )


