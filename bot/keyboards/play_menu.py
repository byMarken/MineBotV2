from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.services.bet_manager import bet_manager
 # здесь безопасно

def create_play_menu(user_id: int) -> ReplyKeyboardMarkup:
    bet_text = bet_manager.get_menu_button(user_id)
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📕 Правила"), KeyboardButton(text="🕹️ Играть")],
            [KeyboardButton(text=bet_text)],
            [KeyboardButton(text="⬅️ Назад в режимы")]
        ],
        resize_keyboard=True
    )
