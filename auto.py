#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OZON AUTO ANSWERER
Автоматически копирует отзывы, вставляет в Claude, ждет ответа,
копирует ответ и вставляет в Ozon
"""

import pyperclip
import pyautogui
import time
import webbrowser
import subprocess
import sys
import os

# Установка зависимостей
try:
    import pyperclip
except ImportError:
    print("Установка pyperclip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyperclip"])
    import pyperclip


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    print("""
╔════════════════════════════════════════════════════════╗
║                                                        ║
║  OZON AUTO ANSWERER                                    ║
║  Автоматический ответчик на отзывы                    ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
""")


def setup_windows():
    """Подготовка окон браузеров"""
    clear()
    print_banner()

    print("""
⚠️  ПОДГОТОВКА К АВТОМАТИЗАЦИИ

Следуйте инструкциям:

1️⃣  Откройте Ozon в браузере (Chrome)
    URL: https://seller.ozon.ru/app/reviews
    Разместите окно на ЛЕВОЙ половине экрана

2️⃣  Откройте Claude в ДРУГОМ браузере (или вкладке)
    URL: https://claude.ai
    Разместите окно на ПРАВОЙ половине экрана

3️⃣  Убедитесь, что вы авторизованы в обоих сервисах

4️⃣  Скопируйте ПЕРВЫЙ ОТЗЫВ со страницы Ozon (Ctrl+C)

5️⃣  Нажмите ENTER в этой программе для начала
""")

    input("\n>>> Нажмите ENTER когда всё готово...")


def get_reviews_from_file():
    """Загружает отзывы из файла"""
    if os.path.exists("reviews.txt"):
        with open("reviews.txt", "r", encoding="utf-8") as f:
            reviews = [line.strip() for line in f if line.strip()]
            return reviews
    return []


def paste_text(text, delay=0.5):
    """Вставляет текст через буфер обмена"""
    try:
        pyperclip.copy(text)
        time.sleep(delay)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(delay)
        return True
    except Exception as e:
        print(f"[ERROR] Ошибка при вставке: {e}")
        return False


def copy_text():
    """Копирует текст из буфера обмена"""
    try:
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        text = pyperclip.paste()
        return text
    except Exception as e:
        print(f"[ERROR] Ошибка при копировании: {e}")
        return ""


def wait_for_claude_answer(timeout=120):
    """Ждет ответа от Claude"""
    print("[⏳] Ожидаю ответ от Claude...")
    print(f"    Жду до {timeout} секунд...")
    print("\n💡 Подсказка: Claude должен закончить генерировать ответ")
    print("   Вы увидите когда кнопка отправки станет активной\n")

    for i in range(timeout):
        if i % 10 == 0:
            print(f"    ⏳ Ещё {timeout - i} секунд...")
        time.sleep(1)

    print("[✓] Время истекло или ответ готов!")
    return True


def click_send_button():
    """Нажимает кнопку отправки (примерная позиция)"""
    try:
        # Ищем и кликаем кнопку отправки
        pyautogui.press('enter')  # Для Ozon форм
        time.sleep(1)
        print("[✓] Нажата кнопка отправки")
        return True
    except Exception as e:
        print(f"[WARNING] Не удалось нажать кнопку: {e}")
        return False


def process_review(review_num, review_text):
    """Обрабатывает один отзыв"""
    print(f"\n{'='*60}")
    print(f"ОТЗЫВ #{review_num}")
    print(f"{'='*60}")

    print(f"\n[1/5] 📋 Текст отзыва ({len(review_text)} символов):")
    print(f"      {review_text[:100]}...")

    # Вставляем в Claude
    print(f"\n[2/5] 💬 Вставляю отзыв в Claude...")
    print("      ⏳ Переключитесь на Claude если нужно")

    if paste_text(review_text, delay=0.5):
        print("      ✓ Отзыв вставлен в Claude")
    else:
        print("      ✗ Ошибка при вставке")
        return None

    # Нажимаем Enter в Claude
    print(f"\n[3/5] 📤 Отправляю запрос в Claude...")
    time.sleep(1)
    pyautogui.press('enter')
    print("      ✓ Запрос отправлен")

    # Ждем ответ
    wait_for_claude_answer(timeout=120)

    # Копируем ответ
    print(f"\n[4/5] 📋 Копирую ответ из Claude...")
    time.sleep(2)
    answer = copy_text()

    if answer and len(answer) > 10:
        print(f"      ✓ Ответ скопирован ({len(answer)} символов)")
        print(f"      Начало: {answer[:80]}...")
        return answer
    else:
        print("      ✗ Ответ не скопирован или слишком короткий")
        return None


def send_answer_to_ozon(answer):
    """Отправляет ответ на Ozon"""
    print(f"\n[5/5] 📝 Вставляю ответ в Ozon...")
    print("      ⏳ Переключитесь на Ozon если нужно")

    # Кликаем в поле ответа (примерно по центру экрана)
    pyautogui.click(400, 400)
    time.sleep(0.5)

    # Вставляем ответ
    if paste_text(answer, delay=0.5):
        print("      ✓ Ответ вставлен в форму")
    else:
        print("      ✗ Ошибка при вставке ответа")
        return False

    # Нажимаем кнопку отправки
    print(f"\n      🔍 Ищу кнопку 'Отправить'...")
    print("      ⚠️  ВРУЧНУЮ нажмите кнопку 'Отправить' на сайте")
    print("      или нажмите SPACE в этой программе чтобы попытаться автоматически")

    input("      >>> Нажмите ENTER когда отправите...")

    print("      ✓ Ответ отправлен!")
    return True


def main():
    """Главная функция"""
    try:
        clear()
        print_banner()

        # Подготовка
        setup_windows()

        # Загружаем отзывы из буфера обмена
        first_review = pyperclip.paste()

        if not first_review or len(first_review) < 10:
            print("\n❌ Ошибка: Не найден первый отзыв в буфере обмена!")
            print("   Пожалуйста, скопируйте отзыв со страницы Ozon (Ctrl+C)")
            input("\n>>> Нажмите ENTER для выхода...")
            return

        # Главный цикл обработки
        reviews = [first_review]
        review_num = 0

        while True:
            review_num += 1

            # Обрабатываем отзыв
            answer = process_review(review_num, reviews[review_num - 1])

            if answer:
                # Отправляем ответ
                send_answer_to_ozon(answer)

                print(f"\n✅ Отзыв #{review_num} обработан успешно!\n")
            else:
                print(f"\n⚠️  Отзыв #{review_num} пропущен\n")

            # Спрашиваем про следующий
            print("\n" + "="*60)
            print("СЛЕДУЮЩИЙ ОТЗЫВ")
            print("="*60)

            choice = input("""
Что дальше?
  [1] Обработать следующий отзыв (скопируйте его сначала)
  [0] Выход

>>> Выберите (0-1): """).strip()

            if choice == "0":
                print("\n✅ Спасибо за использование! До встречи!\n")
                break
            elif choice == "1":
                print("\n[*] Скопируйте следующий отзыв и нажмите ENTER...")
                input(">>> Нажмите ENTER когда скопируете отзыв...")
                next_review = pyperclip.paste()

                if next_review and len(next_review) > 10:
                    reviews.append(next_review)
                    continue
                else:
                    print("❌ Отзыв не скопирован!")
                    break
            else:
                print("❌ Неверный выбор")
                continue

    except KeyboardInterrupt:
        print("\n\n❌ Программа прервана пользователем\n")
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}\n")
        import traceback
        traceback.print_exc()
        input(">>> Нажмите ENTER для выхода...")


if __name__ == "__main__":
    main()
