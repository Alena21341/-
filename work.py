#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OZON REVIEWS - ПОМОЩНИК ДЛЯ ОТВЕТОВ
Правильная версия - помогает вам процесс, вы контролируете
"""

import subprocess
import sys
import os

# Установка pyperclip если нужно
try:
    import pyperclip
except ImportError:
    print("Установка pyperclip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyperclip"])
    import pyperclip

import webbrowser
import time


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_banner():
    print("""
╔════════════════════════════════════════════════════════╗
║                                                        ║
║        OZON REVIEWS HELPER                             ║
║        Помощник для ответов на отзывы                 ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
""")


def wait():
    input("\n>>> Нажмите Enter для продолжения...")


def process_single_review():
    """Обработка одного отзыва - пошагово"""
    clear()
    show_banner()

    print("""
╔════════════════════════════════════════════════════════╗
║                ОБРАБОТКА ОТЗЫВА                       ║
╚════════════════════════════════════════════════════════╝
""")

    # ШАГ 1
    print("\n[1/6] СКОПИРУЙТЕ ОТЗЫВ со страницы Ozon\n")
    print("Инструкция:")
    print("  • Откройте страницу https://seller.ozon.ru/app/reviews")
    print("  • Найдите отзыв который хотите обработать")
    print("  • Выделите текст отзыва мышкой")
    print("  • Нажмите Ctrl+C чтобы скопировать")
    print("\n💡 ПРОВЕРКА: Текст отзыва должен быть в буфере обмена")

    input("\n>>> Нажмите Enter когда скопировали отзыв...")

    # Проверяем что скопировалось
    review = pyperclip.paste()

    if not review or len(review) < 10:
        print("\n❌ Ошибка: Отзыв не скопирован!")
        print("Попробуйте снова:")
        print("  1. Кликните на отзыв в Ozon")
        print("  2. Выделите текст (Ctrl+A)")
        print("  3. Скопируйте (Ctrl+C)")
        return None

    print(f"\n✅ Отзыв скопирован! ({len(review)} символов)")
    print(f"Начало: {review[:100]}...")

    # ШАГ 2
    print("\n\n[2/6] ОТКРОЙТЕ CLAUDE\n")
    print("Нажимаю кнопку чтобы открыть Claude...")
    webbrowser.open("https://claude.ai")
    print("✅ Claude должен открыться в браузере")

    print("\nИнструкция:")
    print("  • Дождитесь загрузки Claude")
    print("  • Убедитесь что вы авторизованы")
    print("  • Кликните в поле ввода сообщения")

    input("\n>>> Нажмите Enter когда Claude готов...")

    # ШАГ 3
    print("\n[3/6] ВСТАВЬТЕ ОТЗЫВ В CLAUDE\n")
    print("Действия:")
    print("  • Кликните в поле ввода Claude")
    print("  • Нажмите Ctrl+V чтобы вставить отзыв")
    print("  • Нажмите SPACE чтобы отправить (или Enter)")

    print("\nПовтор инструкции:")
    print("  1. Убедитесь что курсор в поле ввода Claude")
    print("  2. Нажмите Ctrl+V (вставить)")
    print("  3. Нажмите Enter (отправить)")

    input("\n>>> Нажмите Enter когда вставили отзыв в Claude...")

    # ШАГ 4
    print("\n[4/6] ЖДЕМ ОТВЕТ ОТ CLAUDE\n")
    print("⏳ Claude генерирует ответ...")
    print("\nОжидание может занять:")
    print("  • Быстро: 30 секунд")
    print("  • Норма: 1-2 минуты")
    print("  • Медленно: 3-5 минут")
    print("\nКогда Claude закончит, вы увидите полный ответ в окне.")

    input("\n>>> Нажмите Enter когда ответ готов в Claude...")

    # ШАГ 5
    print("\n[5/6] СКОПИРУЙТЕ ОТВЕТ ИЗ CLAUDE\n")
    print("Инструкция:")
    print("  • В Claude выделите весь ответ (Ctrl+A)")
    print("  • Скопируйте ответ (Ctrl+C)")
    print("  • Вернитесь в эту программу")

    input("\n>>> Нажмите Enter когда скопировали ответ...")

    # Проверяем что скопировалось
    answer = pyperclip.paste()

    if not answer or len(answer) < 10:
        print("\n❌ Ошибка: Ответ не скопирован!")
        print("Попробуйте:")
        print("  1. Кликните на ответ в Claude")
        print("  2. Выделите (Ctrl+A)")
        print("  3. Скопируйте (Ctrl+C)")
        return None

    print(f"\n✅ Ответ скопирован! ({len(answer)} символов)")
    print(f"Начало: {answer[:100]}...")

    # ШАГ 6
    print("\n[6/6] ВСТАВЬТЕ ОТВЕТ НА OZON\n")
    print("Действия:")
    print("  • Откройте вкладку Ozon в браузере")
    print("  • Найдите отзыв который обрабатывали")
    print("  • Кликните в поле 'Ответить' или 'Ответ продавца'")
    print("  • Нажмите Ctrl+V чтобы вставить ответ")
    print("  • Проверьте что ответ вставился правильно")
    print("  • Нажмите кнопку 'Отправить'")

    print("\nПовтор:")
    print("  1. Перейти на Ozon")
    print("  2. Найти форму ответа на отзыв")
    print("  3. Кликнуть в поле (Ctrl+V вставить)")
    print("  4. Нажать 'Отправить'")

    input("\n>>> Нажмите Enter когда отправили ответ на Ozon...")

    print("\n" + "=" * 60)
    print("✅ ОТЗЫВ УСПЕШНО ОБРАБОТАН!")
    print("=" * 60)

    return True


def main():
    """Главная функция"""
    try:
        while True:
            clear()
            show_banner()

            print("ВЫБЕРИТЕ ДЕЙСТВИЕ:\n")
            print("  [1] Обработать один отзыв (пошаговая помощь)")
            print("  [2] Открыть Ozon")
            print("  [3] Открыть Claude")
            print("  [0] Выход\n")

            choice = input(">>> Введите номер (0-3): ").strip()

            if choice == "0":
                clear()
                print("\n✅ Спасибо за использование! До встречи!\n")
                break

            elif choice == "1":
                result = process_single_review()
                if result:
                    print("\nОтзыв обработан успешно!")
                    input("\n>>> Нажмите Enter для главного меню...")

            elif choice == "2":
                print("\n[*] Открываю Ozon...")
                webbrowser.open("https://seller.ozon.ru/app/reviews")
                print("✅ Ozon открыт в браузере!")
                wait()

            elif choice == "3":
                print("\n[*] Открываю Claude...")
                webbrowser.open("https://claude.ai")
                print("✅ Claude открыт в браузере!")
                wait()

            else:
                print("\n❌ Неверный выбор")
                wait()

    except KeyboardInterrupt:
        print("\n\n❌ Программа прервана\n")
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}\n")
        import traceback
        traceback.print_exc()
        input(">>> Нажмите Enter для выхода...")


if __name__ == "__main__":
    main()
