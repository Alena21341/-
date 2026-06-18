#!/usr/bin/env python3
"""
Модуль для работы с Claude API
"""

from anthropic import Anthropic
import os


class ClaudeAPI:
    def __init__(self, api_key=None):
        """Инициализирует Claude API клиент"""
        if api_key:
            os.environ["ANTHROPIC_API_KEY"] = api_key
            self.api_key = api_key
        else:
            self.api_key = os.getenv("ANTHROPIC_API_KEY")

        if not self.api_key:
            raise ValueError("Claude API ключ не установлен")

        self.client = Anthropic()
        self.conversation_history = []

    def generate_response(self, review_text, system_prompt=None):
        """Генерирует ответ на отзыв"""
        if not system_prompt:
            system_prompt = """Вы - помощник продавца на Ozon.
Ваша задача написать вежливый и профессиональный ответ на отзыв покупателя.
Ответ должен быть:
- Кратким (2-3 предложения)
- Вежливым и благодарным
- Решением проблемы (если она есть)
- На русском языке
Напишите только ответ без дополнительного текста."""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Отзыв покупателя:\n\n{review_text}\n\nНапишите ответ на этот отзыв:"
                    }
                ]
            )

            response_text = message.content[0].text
            return response_text.strip()

        except Exception as e:
            raise Exception(f"Ошибка при работе с Claude API: {str(e)}")

    def set_api_key(self, api_key):
        """Устанавливает новый API ключ"""
        os.environ["ANTHROPIC_API_KEY"] = api_key
        self.api_key = api_key
        self.client = Anthropic()

    def validate_api_key(self):
        """Проверяет валидность API ключа"""
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=10,
                messages=[
                    {
                        "role": "user",
                        "content": "Тест"
                    }
                ]
            )
            return True
        except:
            return False


class AdvancedClaudeAPI(ClaudeAPI):
    """Расширенная версия с поддержкой длительных бесед"""

    def __init__(self, api_key=None):
        super().__init__(api_key)
        self.conversation_history = []

    def add_to_history(self, role, content):
        """Добавляет сообщение в историю"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })

    def generate_response_with_history(self, user_message):
        """Генерирует ответ с учетом истории"""
        self.add_to_history("user", user_message)

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=self.conversation_history
            )

            assistant_message = response.content[0].text
            self.add_to_history("assistant", assistant_message)

            return assistant_message
        except Exception as e:
            raise Exception(f"Ошибка: {str(e)}")

    def clear_history(self):
        """Очищает историю разговора"""
        self.conversation_history = []
