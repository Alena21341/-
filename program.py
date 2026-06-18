#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OZON REVIEWS HELPER
Одна простая программа для работы с отзывами Ozon и Claude
"""

import webbrowser
import subprocess
import sys
import os

# Установка pyperclip если нужно
try:
    import pyperclip
except ImportError:
    print("Устанавливаю необходимый модуль...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyperclip"])
    import pyperclip


def clear():
    """Очистить экран"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Пауза"""
    input("\n>>> Нажмите Enter для продолжения...")


def show_banner():
    """Баннер программы"""
    print("""
╔═══════════════════════════════════════════════════╗
║                                                   ║
║     OZON REVIEWS HELPER                           ║
║     Помощник для ответов на отзывы Ozon          ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
""")


def menu():
    """Главное меню"""
    while True:
        clear()
        show_banner()

        print("ВЫБЕРИТЕ ДЕЙСТВИЕ:\n")
        print("  [1] 🌐 Открыть Ozon (отзывы)")
        print("  [2] 💬 Открыть Claude")
        print("  [3] 📋 Показать что в буфере обмена")
        print("  [4] 📝 Инструкция")
        print("  [0] ❌ Выход\n")

        choice = input("Введите номер (0-4): ").strip()

        if choice == "1":
            open_ozon()
        elif choice == "2":
            open_claude()
        elif choice == "3":
            show_buffer()
        elif choice == "4":
            show_help()
        elif choice == "0":
            clear()
            print("Спасибо за использование! 👋\n")
            sys.exit(0)
        else:
            print("\n❌ Неверный выбор, попробуйте снова")
            pause()


def open_ozon():
    """Открыть Ozon"""
    clear()
    show_banner()
    print("⏳ Открываю Ozon в браузере...")
    try:
        webbrowser.open("https://seller.ozon.ru/app/reviews")
        print("✅ Ozon открыт!\n")
        print("Инструкция:")
        print("  1. Дождитесь загрузки страницы")
        print("  2. Найдите отзыв, на который хотите ответить")
        print("  3. Выделите текст отзыва мышкой")
        print("  4. Скопируйте (Ctrl+A, Ctrl+C)")
        print("  5. Вернитесь в эту программу")
        print("  6. Нажмите [3] чтобы увидеть отзыв\n")
    except Exception as e:
        print(f"❌ Ошибка: {e}\n")
    pause()


def open_claude():
    """Открыть Claude"""
    clear()
    show_banner()
    print("⏳ Открываю Claude в браузере...")
    try:
        webbrowser.open("https://claude.ai")
        print("✅ Claude открыт!\n")
        print("Инструкция:")
        print("  1. Дождитесь загрузки Claude")
        print("  2. Вставьте отзыв (Ctrl+V)")
        print("  3. Если нужно, отредактируйте запрос")
        print("  4. Нажмите Enter для отправки")
        print("  5. Получите ответ от Claude")
        print("  6. Выделите ответ (Ctrl+A)")
        print("  7. Скопируйте ответ (Ctrl+C)")
        print("  8. Вернитесь в эту программу\n")
    except Exception as e:
        print(f"❌ Ошибка: {e}\n")
    pause()


def show_buffer():
    """Показать буфер обмена"""
    clear()
    show_banner()

    try:
        text = pyperclip.paste()

        if not text:
            print("❌ Буфер обмена пуст!\n")
        else:
            length = len(text)
            preview = text[:300] if len(text) > 300 else text

            print(f"📋 В БУФЕРЕ ОБМЕНА ({length} символов):\n")
            print("─" * 50)
            print(preview)
            if length > 300:
                print(f"\n... [ещё {length - 300} символов]")
            print("─" * 50)
            print()

            print("💡 ЧТО ДАЛЬШЕ:\n")
            if "спасибо" in text.lower() or "отзыв" in text.lower() or "заказ" in text.lower():
                print("  ✓ Это выглядит как ОТЗЫВ")
                print("  → Откройте Claude [2]")
                print("  → Вставьте отзыв в Claude (Ctrl+V)")
                print("  → Получите ответ")
                print("  → Скопируйте ответ (Ctrl+A, Ctrl+C)")
                print("  → Вернитесь на Ozon")
                print("  → Вставьте ответ в форму (Ctrl+V)")
                print("  → Отправьте!")
            else:
                print("  → Скопируйте эту информацию в нужное место (Ctrl+V)")

    except Exception as e:
        print(f"❌ Ошибка при чтении буфера: {e}\n")

    pause()


def show_help():
    """Показать справку"""
    clear()
    show_banner()

    print("""
╔═══════════════════════════════════════════════════╗
║              ПОЛНАЯ ИНСТРУКЦИЯ                    ║
╚═══════════════════════════════════════════════════╝

ПРОЦЕСС РАБОТЫ:

1️⃣  ОТКРОЙТЕ OZON
    └─ Нажмите [1] в программе
    └─ Откроется страница с отзывами

2️⃣  СКОПИРУЙТЕ ОТЗЫВ
    └─ На странице найдите отзыв
    └─ Выделите текст отзыва (мышкой)
    └─ Скопируйте его (Ctrl+A, Ctrl+C)
    └─ Вернитесь в программу

3️⃣  ПРОВЕРЬТЕ БУФЕР
    └─ Нажмите [3] чтобы увидеть отзыв
    └─ Убедитесь, что отзыв скопирован правильно

4️⃣  ОТКРОЙТЕ CLAUDE
    └─ Нажмите [2] в программе
    └─ Откроется Claude в браузере

5️⃣  ВСТАВЬТЕ ОТЗЫВ В CLAUDE
    └─ В Claude вставьте отзыв (Ctrl+V)
    └─ Если нужно, отредактируйте запрос
    └─ Нажмите Enter

6️⃣  ПОЛУЧИТЕ ОТВЕТ
    └─ Claude генерирует ответ
    └─ Подождите пока ответ готов
    └─ Выделите весь ответ (Ctrl+A)
    └─ Скопируйте ответ (Ctrl+C)

7️⃣  ВЕРНИТЕСЬ НА OZON
    └─ Переключитесь на Ozon (Alt+Tab)
    └─ Найдите форму для ответа на отзыв

8️⃣  ВСТАВЬТЕ ОТВЕТ
    └─ Кликните в поле для ответа
    └─ Вставьте ответ (Ctrl+V)
    └─ Проверьте текст

9️⃣  ОТПРАВЬТЕ
    └─ Нажмите кнопку "Отправить"
    └─ Ответ отправлен!

ПОВТОРИТЕ для следующего отзыва!

СОВЕТЫ:
  • Alt+Tab - быстрое переключение между окнами
  • Ctrl+C - копирование
  • Ctrl+V - вставка
  • Ctrl+A - выделить всё
  • [3] - проверить что в буфере обмена
""")

    pause()


def main():
    """Главная функция"""
    try:
        menu()
    except KeyboardInterrupt:
        clear()
        print("\n\n❌ Программа прервана пользователем\n")
        sys.exit(0)
    except Exception as e:
        clear()
        print(f"\n❌ ОШИБКА: {e}\n")
        import traceback
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")
        sys.exit(1)


if __name__ == "__main__":
    main()
