# utils.py

from aiogram import Bot
from aiogram.types import Message
from typing import List


# Хранилище сообщений для каждого чата
user_messages = {}

async def clear_chat(bot: Bot, user_id: int, chat_id: int):
    """Функция для удаления старых сообщений, отправленных ботом"""
    if user_id in user_messages:
        old_messages = user_messages.pop(user_id)
        for msg_id in old_messages:
            try:
                # Получаем сообщение и проверяем, что это сообщение бота
                msg = await bot.get_message(chat_id=chat_id, message_id=msg_id)
                if msg.from_user.id == bot.id:  # Проверяем, что это сообщение бота
                    await bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")

def store_message(user_id: int, msg_id: int):
    """Функция для сохранения ID сообщений, отправленных ботом"""
    if user_id not in user_messages:
        user_messages[user_id] = []
    user_messages[user_id].append(msg_id)
