from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def beautiful_balance(value: float | int) -> str:
    return f"{int(value):,}".replace(",", ".")

def create_bet_keyboard(current_bet: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➖", callback_data="decrease_bet"),
            InlineKeyboardButton(text=f"{current_bet} 💎", callback_data="current_bet"),
            InlineKeyboardButton(text="➕", callback_data="increase_bet"),
        ]
    ])


class BetManager:
    def __init__(self, start_bet: int = 100, step: int = 50, min_bet: int = 50, max_bet: int = 1_000_000_000):
        self.bet = start_bet
        self.step = step
        self.min_bet = min_bet
        self.max_bet = max_bet

    def increase(self):
        self.bet = min(self.max_bet, self.bet + self.step)

    def decrease(self):
        self.bet = max(self.min_bet, self.bet - self.step)

    def get_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data="decrease_bet"),
                InlineKeyboardButton(text=f"{self.bet} 💎", callback_data="noop"),
                InlineKeyboardButton(text="➕", callback_data="increase_bet"),
            ]
        ])
