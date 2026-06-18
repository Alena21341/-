#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, sys, os, webbrowser, time
try:
    import pyperclip
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyperclip"])
    import pyperclip

def clear(): os.system('cls' if os.name == 'nt' else 'clear')
def banner():
    print("""
╔══════════════════════════════════════════════════════╗
║  OZON REVIEWS HELPER - ВСЁ В ОДНОМ СКРИПТЕ         ║
╚══════════════════════════════════════════════════════╝
""")

def menu():
    while True:
        clear()
        banner()
        print("ГЛАВНОЕ МЕНЮ:\n")
        print("  [1] Обработать отзыв (пошагово)")
        print("  [2] Открыть Ozon")
        print("  [3] Открыть Claude")
        print("  [0] Выход\n")

        c = input(">>> Выбор (0-3): ").strip()

        if c == "0":
            clear()
            print("\n✅ До встречи!\n")
            break
        elif c == "1":
            process()
        elif c == "2":
            webbrowser.open("https://seller.ozon.ru/app/reviews")
            print("✅ Ozon открыт")
            input("\n>>> Enter...")
        elif c == "3":
            webbrowser.open("https://claude.ai")
            print("✅ Claude открыт")
            input("\n>>> Enter...")

def process():
    clear()
    banner()
    print("=" * 60)
    print("ОБРАБОТКА ОТЗЫВА - СЛЕДУЙТЕ ИНСТРУКЦИЯМ")
    print("=" * 60)

    # ШАГ 1
    print("\n[1/6] СКОПИРУЙТЕ ОТЗЫВ\n")
    print("  1. Откройте Ozon: https://seller.ozon.ru/app/reviews")
    print("  2. Найдите отзыв")
    print("  3. Выделите текст (мышкой)")
    print("  4. Скопируйте (Ctrl+C)")
    input("\n>>> Нажмите Enter когда скопировали...")

    review = pyperclip.paste()
    if not review or len(review) < 10:
        print("❌ Отзыв не найден в буфере!")
        input("\n>>> Enter...")
        return

    print(f"✅ Отзыв скопирован ({len(review)} символов)")

    # ШАГ 2
    print("\n[2/6] ОТКРЫВАЮ CLAUDE...")
    webbrowser.open("https://claude.ai")
    print("✅ Claude откроется в браузере")
    input("\n>>> Когда Claude загрузился - Enter...")

    # ШАГ 3
    print("\n[3/6] ВСТАВЬТЕ ОТЗЫВ В CLAUDE\n")
    print("  1. Кликните в поле ввода Claude")
    print("  2. Нажмите Ctrl+V (вставить отзыв)")
    print("  3. Нажмите Enter (отправить)")
    input("\n>>> Нажмите Enter когда отправили запрос...")

    # ШАГ 4
    print("\n[4/6] ОЖИДАНИЕ ОТВЕТА\n")
    print("⏳ Claude генерирует ответ (1-5 минут)...")
    print("\n   Программа будет ждать пока вы скажете что готово")
    input("\n>>> Когда ответ в Claude готов - Enter...")

    # ШАГ 5
    print("\n[5/6] СКОПИРУЙТЕ ОТВЕТ\n")
    print("  1. В Claude выделите весь ответ (Ctrl+A)")
    print("  2. Скопируйте (Ctrl+C)")
    input("\n>>> Нажмите Enter когда скопировали ответ...")

    answer = pyperclip.paste()
    if not answer or len(answer) < 10:
        print("❌ Ответ не найден!")
        input("\n>>> Enter...")
        return

    print(f"✅ Ответ скопирован ({len(answer)} символов)")

    # ШАГ 6
    print("\n[6/6] ВСТАВЬТЕ ОТВЕТ НА OZON\n")
    print("  1. Откройте Ozon")
    print("  2. Найдите форму ответа на отзыв")
    print("  3. Кликните в поле ответа")
    print("  4. Нажмите Ctrl+V (вставить ответ)")
    print("  5. Нажмите кнопку 'Отправить'")
    input("\n>>> Когда отправили - Enter...")

    print("\n" + "=" * 60)
    print("✅ ОТЗЫВ УСПЕШНО ОБРАБОТАН!")
    print("=" * 60)
    input("\n>>> Enter для меню...")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n❌ Прервано\n")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}\n")
