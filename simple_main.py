#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ozon Reviews Helper - Простая версия для копирования отзывов и ответов
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyperclip
import subprocess
import webbrowser
import os

class SimpleOzonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ozon Reviews Helper")
        self.root.geometry("900x600")

        # Данные
        self.reviews = []
        self.current_index = 0
        self.clipboard_history = []

        self.setup_ui()
        print("[OK] Приложение запущено успешно!")

    def setup_ui(self):
        """Создает интерфейс"""

        # ===== ВЕРХНЯЯ ПАНЕЛЬ =====
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(top_frame, text="Ozon Reviews Helper", font=("Arial", 14, "bold")).pack(side=tk.LEFT)

        # ===== ЛЕВАЯ ПАНЕЛЬ - УПРАВЛЕНИЕ =====
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Кнопки браузера
        ttk.Label(left_frame, text="Браузер:", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 5))

        ttk.Button(left_frame, text="🌐 Открыть Ozon", command=self.open_ozon).pack(fill=tk.X, pady=2)
        ttk.Button(left_frame, text="💬 Открыть Claude", command=self.open_claude).pack(fill=tk.X, pady=2)

        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Работа с текстом
        ttk.Label(left_frame, text="Копирование:", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 5))

        ttk.Button(left_frame, text="📋 Вставить из Ozon", command=self.paste_from_ozon).pack(fill=tk.X, pady=2)
        ttk.Button(left_frame, text="📋 Скопировать отзыв", command=self.copy_review).pack(fill=tk.X, pady=2)
        ttk.Button(left_frame, text="📋 Вставить ответ", command=self.paste_answer).pack(fill=tk.X, pady=2)
        ttk.Button(left_frame, text="📋 Скопировать ответ", command=self.copy_answer).pack(fill=tk.X, pady=2)

        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Примеры
        ttk.Label(left_frame, text="Шаблоны ответов:", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 5))

        ttk.Button(left_frame, text="✓ Спасибо за отзыв", command=lambda: self.insert_template("Спасибо за Ваш отзыв! Мы ценим Вашу обратную связь и постараемся улучшить качество.")).pack(fill=tk.X, pady=2)

        ttk.Button(left_frame, text="✓ Извините за проблему", command=lambda: self.insert_template("Приносим извинения за возникшие проблемы. Пожалуйста, напишите нам для решения вопроса.")).pack(fill=tk.X, pady=2)

        # ===== ПРАВАЯ ПАНЕЛЬ - СОДЕРЖИМОЕ =====
        right_frame = ttk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Отзыв
        ttk.Label(right_frame, text="ОТЗЫВ", font=("Arial", 11, "bold")).pack(anchor=tk.W)

        self.review_text = scrolledtext.ScrolledText(right_frame, height=6, wrap=tk.WORD, font=("Courier", 9))
        self.review_text.pack(fill=tk.X, pady=(0, 10))

        # Ответ
        ttk.Label(right_frame, text="ОТВЕТ", font=("Arial", 11, "bold")).pack(anchor=tk.W)

        self.answer_text = scrolledtext.ScrolledText(right_frame, height=6, wrap=tk.WORD, font=("Courier", 9))
        self.answer_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Статус
        self.status_label = ttk.Label(right_frame, text="✓ Готово", foreground="green")
        self.status_label.pack(anchor=tk.W)

    def log(self, msg):
        """Логирование в консоль"""
        print(f"[INFO] {msg}")

    def open_ozon(self):
        """Открывает Ozon"""
        try:
            webbrowser.open("https://seller.ozon.ru/app/reviews")
            self.status_label.config(text="✓ Ozon открыт в браузере", foreground="green")
            self.log("Ozon открыт")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть Ozon: {e}")

    def open_claude(self):
        """Открывает Claude"""
        try:
            webbrowser.open("https://claude.ai")
            self.status_label.config(text="✓ Claude открыт в браузере", foreground="green")
            self.log("Claude открыт")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть Claude: {e}")

    def paste_from_ozon(self):
        """Вставляет из буфера обмена (из Ozon)"""
        try:
            text = pyperclip.paste()
            self.review_text.delete(1.0, tk.END)
            self.review_text.insert(1.0, text)
            self.status_label.config(text="✓ Отзыв вставлен", foreground="green")
            self.log(f"Отзыв вставлен ({len(text)} символов)")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось вставить: {e}")

    def copy_review(self):
        """Копирует отзыв в буфер обмена"""
        try:
            text = self.review_text.get(1.0, tk.END).strip()
            pyperclip.copy(text)
            self.status_label.config(text="✓ Отзыв скопирован в буфер обмена", foreground="green")
            self.log(f"Отзыв скопирован ({len(text)} символов)")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось скопировать: {e}")

    def paste_answer(self):
        """Вставляет ответ из буфера обмена"""
        try:
            text = pyperclip.paste()
            self.answer_text.delete(1.0, tk.END)
            self.answer_text.insert(1.0, text)
            self.status_label.config(text="✓ Ответ вставлен", foreground="green")
            self.log(f"Ответ вставлен ({len(text)} символов)")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось вставить: {e}")

    def copy_answer(self):
        """Копирует ответ в буфер обмена"""
        try:
            text = self.answer_text.get(1.0, tk.END).strip()
            pyperclip.copy(text)
            self.status_label.config(text="✓ Ответ скопирован в буфер обмена", foreground="green")
            self.log(f"Ответ скопирован ({len(text)} символов)")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось скопировать: {e}")

    def insert_template(self, template):
        """Вставляет шаблон в поле ответа"""
        self.answer_text.insert(tk.END, template)
        self.log(f"Шаблон добавлен: {template[:30]}...")


def main():
    root = tk.Tk()
    app = SimpleOzonApp(root)
    root.mainloop()


if __name__ == "__main__":
    print("=" * 50)
    print("Ozon Reviews Helper - ЗАПУСК")
    print("=" * 50)
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")
