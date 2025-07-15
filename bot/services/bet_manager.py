from typing import Dict

class BetManager:
    def __init__(self):
        self._bets: Dict[int, int] = {}
        self.default_bet = 10

    def get_bet(self, user_id: int) -> int:
        return self._bets.get(user_id, self.default_bet)

    def set_bet(self, user_id: int, amount: int):
        self._bets[user_id] = amount

    def get_menu_button(self, user_id: int) -> str:
        return f"💵 Ставка: {self.get_bet(user_id)}$"

# Экземпляр менеджера
bet_manager = BetManager()
