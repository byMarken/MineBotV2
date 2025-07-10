import requests
import re
import os
import time

BASE_API_URL = "http://localhost:8000/dep"

def follow(thefile):
    thefile.seek(0, 2)  # Переходим в конец файла
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def parse_payment(line):
    match = re.search(r"\[CHAT\].*?Игрок (\w+) отправил вам ([\d\.]+) монеток", line)
    if match:
        nickname = match.group(1)
        amount = float(match.group(2))
        return nickname, amount
    return None

if __name__ == "__main__":
    log_path = os.path.join(os.getenv("APPDATA"), ".minecraft", "logs", "latest.log")
    with open(log_path, "r", encoding="cp1251", errors="ignore") as logfile:
        loglines = follow(logfile)
        for line in loglines:
            result = parse_payment(line)
            if result:
                nickname, amount = result
                try:
                    response = requests.post(
                        BASE_API_URL,
                        json={"sender": nickname, "amount": amount}
                    )
                    print(f"Статус подтверждения: {response.json()}")
                except Exception as e:
                    print(f"Ошибка отправки: {e}")