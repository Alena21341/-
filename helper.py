#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ozon Reviews Helper - КОНСОЛЬНАЯ ВЕРСИЯ
Самая простая версия без GUI
"""

import webbrowser
import subprocess
import sys
import os

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False
    print("[WARNING] pyperclip не установлен, попробуем установить...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyperclip"])
        import pyperclip
        HAS_PYPERCLIP = True
    except:
        HAS_PYPERCLIP = False


def clear_screen():
    """Очищает экран"""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu():
    """Показывает главное меню"""
    clear_screen()
    print("=" * 50)
    print("  OZON REVIEWS HELPER")
    print("=" * 50)
    print()
    print("БРАУЗЕР:")
    print("  1. Открыть Ozon (отзывы)")
    print("  2. Открыть Claude")
    print()
    print("РАБОТА С БУФЕРОМ ОБМЕНА:")
    print("  3. Показать отзыв из буфера")
    print("  4. Показать ответ из буфера")
    print()
    print("ДРУГОЕ:")
    print("  5. Инструкция")
    print("  0. Выход")
    print()


def open_ozon():
    """Открывает Ozon"""
    print("\n[*] Открываю Ozon...")
    try:
        webbrowser.open("https://seller.ozon.ru/app/reviews")
        print("[✓] Ozon открыт в вашем браузере!")
    except Exception as e:
        print(f"[✗] Ошибка: {e}")
    input("\nНажмите Enter для продолжения...")


def open_claude():
    """Открывает Claude"""
    print("\n[*] Открываю Claude...")
    try:
        webbrowser.open("https://claude.ai")
        print("[✓] Claude открыт в вашем браузере!")
    except Exception as e:
        print(f"[✗] Ошибка: {e}")
    input("\nНажмите Enter для продолжения...")


def show_clipboard():
    """Показывает содержимое буфера обмена"""
    if not HAS_PYPERCLIP:
        print("[✗] pyperclip не установлен!")
        return

    print("\n[*] Содержимое буфера обмена:")
    print("-" * 50)
    try:
        text = pyperclip.paste()
        print(text[:500])
        if len(text) > 500:
            print(f"\n... (всего {len(text)} символов)")
    except Exception as e:
        print(f"[✗] Ошибка: {e}")
    print("-" * 50)
    input("\nНажмите Enter для продолжения...")


def show_instructions():
    """Показывает инструкцию"""
    clear_screen()
    print("=" * 50)
    print("  ИНСТРУКЦИЯ")
    print("=" * 50)
    print("""
1. ОТКРОЙТЕ OZON (кнопка 1)
   - Нажмите "Открыть Ozon"
   - Откроется страница с отзывами

2. СКОПИРУЙТЕ ОТЗЫВ
   - На странице Ozon щелкните на текст отзыва
   - Скопируйте его (Ctrl+A, Ctrl+C)

3. ОТКРОЙТЕ CLAUDE (кнопка 2)
   - Нажмите "Открыть Claude"
   - Откроется Claude.ai

4. ВСТАВЬТЕ ОТЗЫВ В CLAUDE
   - В Claude вставьте отзыв (Ctrl+V)
   - Отредактируйте запрос если нужно
   - Нажмите Enter

5. ПОЛУЧИТЕ ОТВЕТ
   - Claude генерирует ответ
   - Выделите ответ (Ctrl+A)
   - Скопируйте (Ctrl+C)

6. ВСТАВЬТЕ ОТВЕТ В OZON
   - Вернитесь на Ozon
   - Вставьте ответ в форму (Ctrl+V)
   - Нажмите "Отправить"

7. ПОВТОРИТЕ для следующего отзыва!

СОВЕТЫ:
  - Используйте Alt+Tab для переключения между окнами
  - Быстрое копирование: Ctrl+C, Ctrl+V
  - В программе нажимайте кнопку 3 или 4 для проверки буфера
    """)
    input("\nНажмите Enter для выхода...")


def main():
    """Главный цикл программы"""
    while True:
        show_menu()
        choice = input("Выберите действие (0-5): ").strip()

        if choice == "0":
            print("\nДо встречи! 👋")
            break
        elif choice == "1":
            open_ozon()
        elif choice == "2":
            open_claude()
        elif choice == "3":
            print("\n📋 ОТЗЫВ (из буфера обмена):")
            show_clipboard()
        elif choice == "4":
            print("\n📝 ОТВЕТ (из буфера обмена):")
            show_clipboard()
        elif choice == "5":
            show_instructions()
        else:
            print("\n[✗] Неверный выбор, попробуйте снова")
            input("\nНажмите Enter...")


if __name__ == "__main__":
    print("Запуск Ozon Reviews Helper...")
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\n[✗] ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")
