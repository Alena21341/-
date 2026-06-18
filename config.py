#!/usr/bin/env python3
"""
Модуль управления конфигурацией
"""

import json
import os


class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """Загружает конфигурацию из файла"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_default_config()
        return self.get_default_config()

    def get_default_config(self):
        """Возвращает конфигурацию по умолчанию"""
        return {
            "api_key": "",
            "ozon_url": "https://seller.ozon.ru/app/reviews",
            "claude_url": "https://claude.ai",
            "delay": 3,
            "browser": "chrome"
        }

    def save_config(self):
        """Сохраняет конфигурацию в файл"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")
            return False

    def get_api_key(self):
        """Получает API ключ"""
        return self.config.get("api_key", "")

    def set_api_key(self, api_key):
        """Устанавливает API ключ"""
        self.config["api_key"] = api_key
        self.save_config()

    def get_delay(self):
        """Получает задержку"""
        return self.config.get("delay", 3)

    def set_delay(self, delay):
        """Устанавливает задержку"""
        self.config["delay"] = delay
        self.save_config()

    def get(self, key, default=None):
        """Получает значение по ключу"""
        return self.config.get(key, default)

    def set(self, key, value):
        """Устанавливает значение по ключу"""
        self.config[key] = value
        self.save_config()
