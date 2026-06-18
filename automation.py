#!/usr/bin/env python3
"""
Модуль автоматизации браузера и работы с буфером обмена
"""

import pyperclip
import pyautogui
import subprocess
import time
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class OzonAutomation:
    def __init__(self):
        self.driver = None
        self.ozon_driver = None
        self.claude_driver = None
        self.api_key = None
        self.os = platform.system()

    def set_api_key(self, api_key):
        """Устанавливает API ключ Claude"""
        self.api_key = api_key

    def open_ozon(self):
        """Открывает Ozon в браузере"""
        try:
            if self.driver is None:
                print("[DEBUG] Загружаю ChromeDriver...")
                options = webdriver.ChromeOptions()
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("user-agent=Mozilla/5.0")
                options.add_argument("--disable-gpu")
                print("[DEBUG] Создаю Chrome драйвер...")

                self.driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    options=options
                )

            self.ozon_driver = self.driver
            print("[DEBUG] Открываю Ozon страницу...")
            self.driver.get("https://seller.ozon.ru/app/reviews")
            time.sleep(3)
            self.wait_for_page_load()
            print("[DEBUG] Ozon успешно открыт")
        except Exception as e:
            print(f"[ERROR] Ошибка при открытии Ozon: {e}")
            raise

    def open_claude(self):
        """Открывает Claude в браузере"""
        try:
            if self.claude_driver is None:
                print("[DEBUG] Создаю новый драйвер для Claude...")
                options = webdriver.ChromeOptions()
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("--disable-gpu")

                self.claude_driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    options=options
                )

            print("[DEBUG] Открываю Claude...")
            self.claude_driver.get("https://claude.ai")
            time.sleep(2)
            print("[DEBUG] Claude открыт успешно")
        except Exception as e:
            print(f"[ERROR] Ошибка при открытии Claude: {e}")
            raise

    def get_reviews(self):
        """Получает список отзывов со страницы"""
        try:
            print("[DEBUG] Ожидаю загрузки отзывов со страницы...")
            # Ждем загрузки таблицы
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "n1d-d2a"))
                )
            except Exception as wait_error:
                print(f"[WARNING] Селектор n1d-d2a не найден: {wait_error}")
                print("[DEBUG] Пробую альтернативные селекторы...")

            # Находим все элементы отзывов
            review_elements = self.driver.find_elements(By.CLASS_NAME, "n1d-d2a")
            print(f"[DEBUG] Найдено элементов: {len(review_elements)}")

            reviews = []
            for i, element in enumerate(review_elements):
                try:
                    text = element.text.strip()
                    if text:
                        reviews.append({
                            "text": text,
                            "element": element
                        })
                        print(f"[DEBUG] Отзыв {i+1}: {text[:50]}...")
                except Exception as e:
                    print(f"[WARNING] Ошибка при чтении отзыва {i}: {e}")
                    continue

            print(f"[DEBUG] Всего загружено отзывов: {len(reviews)}")
            return reviews
        except Exception as e:
            print(f"[ERROR] Ошибка загрузки отзывов: {e}")
            raise Exception(f"Ошибка загрузки отзывов: {str(e)}")

    def wait_for_page_load(self):
        """Ждет полной загрузки страницы"""
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except:
            time.sleep(2)

    def copy_to_clipboard(self, text):
        """Копирует текст в буфер обмена"""
        try:
            print(f"[DEBUG] Копирую в буфер обмена ({len(text)} символов)...")
            pyperclip.copy(text)
            print("[DEBUG] Текст успешно скопирован")
        except Exception as e:
            print(f"[ERROR] Ошибка копирования: {e}")
            raise Exception(f"Ошибка копирования: {str(e)}")

    def read_clipboard(self):
        """Читает текст из буфера обмена"""
        try:
            print("[DEBUG] Читаю из буфера обмена...")
            text = pyperclip.paste()
            print(f"[DEBUG] Прочитано {len(text)} символов из буфера")
            return text
        except Exception as e:
            print(f"[ERROR] Ошибка чтения буфера: {e}")
            raise Exception(f"Ошибка чтения буфера: {str(e)}")

    def switch_to_claude(self):
        """Переключается на окно Claude"""
        if self.claude_driver:
            self.claude_driver.switch_to.window(self.claude_driver.current_window_handle)

    def switch_to_ozon(self):
        """Переключается на окно Ozon"""
        if self.ozon_driver:
            self.ozon_driver.switch_to.window(self.ozon_driver.current_window_handle)

    def paste(self):
        """Вставляет из буфера обмена (Ctrl+V)"""
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

    def copy(self):
        """Копирует выделенное (Ctrl+C)"""
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)

    def select_all(self):
        """Выделяет всё (Ctrl+A)"""
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)

    def send_answer(self):
        """Отправляет ответ на сайте Ozon"""
        # Находим кнопку отправки и кликаем
        try:
            # Кнопка "Отправить" или "Ответить" - селектор может отличаться
            send_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Отправить') or contains(text(), 'Ответить')]"))
            )
            send_button.click()
        except:
            # Если кнопка не найдена, пробуем клик по Enter
            pyautogui.press('enter')

    def close(self):
        """Закрывает браузеры"""
        if self.ozon_driver:
            self.ozon_driver.quit()
        if self.claude_driver:
            self.claude_driver.quit()
