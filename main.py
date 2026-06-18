#!/usr/bin/env python3
"""
Ozon Reviews Auto Responder
Вставляет отзывы в Claude и ждет вашего ответа
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime
from automation import OzonAutomation
from config import Config

class OzonReviewsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ozon Reviews Auto Responder (Claude вручную)")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)

        self.automation = OzonAutomation()
        self.config = Config()
        self.is_running = False
        self.current_review_index = 0
        self.reviews = []

        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        """Создает интерфейс приложения"""

        # Левая панель - управление
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10)

        # Заголовок
        title_label = ttk.Label(left_frame, text="Управление", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Кнопка открыть Ozon
        self.open_ozon_btn = ttk.Button(left_frame, text="1. Открыть Ozon", command=self.open_ozon)
        self.open_ozon_btn.pack(fill=tk.X, pady=5)

        # Кнопка загрузить отзывы
        self.load_reviews_btn = ttk.Button(left_frame, text="2. Загрузить отзывы", command=self.load_reviews)
        self.load_reviews_btn.pack(fill=tk.X, pady=5)
        self.load_reviews_btn.config(state=tk.DISABLED)

        # Кнопка открыть Claude
        self.open_claude_btn = ttk.Button(left_frame, text="3. Открыть Claude", command=self.open_claude)
        self.open_claude_btn.pack(fill=tk.X, pady=5)

        # Кнопка начать обработку
        self.start_btn = ttk.Button(left_frame, text="4. Начать обработку", command=self.start_automation)
        self.start_btn.pack(fill=tk.X, pady=5)
        self.start_btn.config(state=tk.DISABLED)

        # Кнопка остановить
        self.stop_btn = ttk.Button(left_frame, text="⏹ Остановить", command=self.stop_automation)
        self.stop_btn.pack(fill=tk.X, pady=5)
        self.stop_btn.config(state=tk.DISABLED)

        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        # Процесс обработки
        process_label = ttk.Label(left_frame, text="Процесс", font=("Arial", 12, "bold"))
        process_label.pack(pady=10)

        # Копировать отзыв
        self.copy_review_btn = ttk.Button(left_frame, text="📋 Копировать отзыв", command=self.copy_current_review)
        self.copy_review_btn.pack(fill=tk.X, pady=5)
        self.copy_review_btn.config(state=tk.DISABLED)

        # Вставить в Claude
        self.paste_in_claude_btn = ttk.Button(left_frame, text="💬 Вставить в Claude", command=self.paste_in_claude)
        self.paste_in_claude_btn.pack(fill=tk.X, pady=5)
        self.paste_in_claude_btn.config(state=tk.DISABLED)

        # Копировать ответ из Claude
        self.copy_answer_btn = ttk.Button(left_frame, text="📋 Копировать ответ", command=self.copy_answer)
        self.copy_answer_btn.pack(fill=tk.X, pady=5)
        self.copy_answer_btn.config(state=tk.DISABLED)

        # Вставить в Ozon
        self.paste_in_ozon_btn = ttk.Button(left_frame, text="✏️ Вставить в Ozon", command=self.paste_in_ozon)
        self.paste_in_ozon_btn.pack(fill=tk.X, pady=5)
        self.paste_in_ozon_btn.config(state=tk.DISABLED)

        # Отправить
        self.send_btn = ttk.Button(left_frame, text="✓ Отправить", command=self.send_answer)
        self.send_btn.pack(fill=tk.X, pady=5)
        self.send_btn.config(state=tk.DISABLED)

        # Правая панель - логирование и просмотр отзывов
        right_frame = ttk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Статус
        status_frame = ttk.LabelFrame(right_frame, text="Статус", padding=10)
        status_frame.pack(fill=tk.X, pady=5)

        self.status_label = ttk.Label(status_frame, text="Готово", foreground="green", font=("Arial", 10))
        self.status_label.pack()

        self.progress_label = ttk.Label(status_frame, text="Отзывы: 0/0")
        self.progress_label.pack()

        # Инструкция
        instruction_frame = ttk.LabelFrame(right_frame, text="Инструкция", padding=10)
        instruction_frame.pack(fill=tk.X, pady=5)

        instruction_text = """1. Нажмите кнопки 1-3 для подготовки
2. Кликните "Копировать отзыв"
3. Кликните "Вставить в Claude"
4. Получите ответ в Claude вручную
5. Кликните "Копировать ответ"
6. Кликните "Вставить в Ozon"
7. Кликните "Отправить"
8. Повторите для следующего отзыва"""

        instruction_label = ttk.Label(instruction_frame, text=instruction_text, justify=tk.LEFT)
        instruction_label.pack(anchor=tk.W)

        # Лог
        log_frame = ttk.LabelFrame(right_frame, text="Лог операций", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=70, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Текущий отзыв
        review_frame = ttk.LabelFrame(right_frame, text="Текущий отзыв", padding=5)
        review_frame.pack(fill=tk.X, pady=5)

        self.current_review_text = scrolledtext.ScrolledText(review_frame, height=3, width=70, wrap=tk.WORD)
        self.current_review_text.pack(fill=tk.X)

        # Ответ от Claude
        answer_frame = ttk.LabelFrame(right_frame, text="Ответ из Claude", padding=5)
        answer_frame.pack(fill=tk.X, pady=5)

        self.current_answer_text = scrolledtext.ScrolledText(answer_frame, height=3, width=70, wrap=tk.WORD)
        self.current_answer_text.pack(fill=tk.X)

        # Кнопки управления отзывами
        nav_frame = ttk.Frame(right_frame)
        nav_frame.pack(fill=tk.X, pady=5)

        self.prev_btn = ttk.Button(nav_frame, text="← Предыдущий", command=self.prev_review)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        self.prev_btn.config(state=tk.DISABLED)

        self.next_btn = ttk.Button(nav_frame, text="Следующий →", command=self.next_review)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        self.next_btn.config(state=tk.DISABLED)

    def log(self, message):
        """Добавляет сообщение в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()

    def open_ozon(self):
        """Открывает браузер с Ozon"""
        self.log("Открываю Ozon...")
        try:
            self.automation.open_ozon()
            self.log("✓ Ozon открыт")
            self.load_reviews_btn.config(state=tk.NORMAL)
        except Exception as e:
            self.log(f"✗ Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", str(e))

    def load_reviews(self):
        """Загружает отзывы со страницы"""
        self.log("Загружаю отзывы...")
        try:
            self.reviews = self.automation.get_reviews()
            self.log(f"✓ Загружено {len(self.reviews)} отзывов")
            self.progress_label.config(text=f"Отзывы: 0/{len(self.reviews)}")
            self.current_review_index = 0
            self.show_current_review()
            self.copy_review_btn.config(state=tk.NORMAL)
            self.prev_btn.config(state=tk.NORMAL)
            self.next_btn.config(state=tk.NORMAL)
        except Exception as e:
            self.log(f"✗ Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", str(e))

    def open_claude(self):
        """Открывает Claude"""
        self.log("Открываю Claude...")
        try:
            self.automation.open_claude()
            self.log("✓ Claude открыт в новом окне")
            self.paste_in_claude_btn.config(state=tk.NORMAL)
        except Exception as e:
            self.log(f"✗ Ошибка: {str(e)}")

    def show_current_review(self):
        """Показывает текущий отзыв"""
        if not self.reviews or self.current_review_index < 0:
            return

        if self.current_review_index >= len(self.reviews):
            self.current_review_index = len(self.reviews) - 1

        review = self.reviews[self.current_review_index]
        self.current_review_text.delete(1.0, tk.END)
        self.current_review_text.insert(1.0, review.get('text', ''))
        self.progress_label.config(text=f"Отзывы: {self.current_review_index + 1}/{len(self.reviews)}")

    def copy_current_review(self):
        """Копирует текущий отзыв в буфер обмена"""
        if not self.reviews:
            messagebox.showwarning("Предупреждение", "Сначала загрузите отзывы")
            return

        review_text = self.reviews[self.current_review_index].get('text', '')
        try:
            self.automation.copy_to_clipboard(review_text)
            self.log(f"✓ Отзыв #{self.current_review_index + 1} скопирован")
            self.paste_in_claude_btn.config(state=tk.NORMAL)
        except Exception as e:
            self.log(f"✗ Ошибка копирования: {str(e)}")

    def paste_in_claude(self):
        """Вставляет отзыв в Claude"""
        self.log("Переключитесь на Claude и нажмите кнопку вставки")
        self.log("Или просто нажмите Ctrl+V в Claude")
        try:
            self.automation.switch_to_claude()
            time.sleep(0.5)
            self.automation.paste()
            self.log("✓ Отзыв вставлен в Claude")
            self.copy_answer_btn.config(state=tk.NORMAL)
        except Exception as e:
            self.log(f"✗ Ошибка: {str(e)}")

    def copy_answer(self):
        """Копирует ответ из Claude"""
        self.log("Выделите ответ в Claude (Ctrl+A) и скопируйте (Ctrl+C)")
        try:
            # Даем время пользователю выделить текст
            time.sleep(1)
            answer = self.automation.read_clipboard()
            self.current_answer_text.delete(1.0, tk.END)
            self.current_answer_text.insert(1.0, answer)
            self.log("✓ Ответ скопирован")
            self.paste_in_ozon_btn.config(state=tk.NORMAL)
        except Exception as e:
            self.log(f"✗ Ошибка: {str(e)}")

    def paste_in_ozon(self):
        """Вставляет ответ в Ozon"""
        try:
            self.automation.switch_to_ozon()
            time.sleep(0.5)
            self.automation.paste()
            self.log("✓ Ответ вставлен в Ozon")
            self.send_btn.config(state=tk.NORMAL)
        except Exception as e:
            self.log(f"✗ Ошибка: {str(e)}")

    def send_answer(self):
        """Отправляет ответ"""
        try:
            self.automation.send_answer()
            self.log("✓ Ответ отправлен")
            self.current_answer_text.delete(1.0, tk.END)
            self.status_label.config(text="Ответ отправлен ✓", foreground="green")

            # Переходим к следующему отзыву
            self.next_review()
        except Exception as e:
            self.log(f"Отправка завершена (нажмите кнопку отправки на сайте вручную)")

    def start_automation(self):
        """Начинает обработку - показывает первый отзыв"""
        if not self.reviews:
            messagebox.showwarning("Предупреждение", "Сначала загрузите отзывы")
            return
        self.current_review_index = 0
        self.show_current_review()
        self.log("✓ Готово к обработке отзывов")

    def next_review(self):
        """Переходит к следующему отзыву"""
        if not self.reviews:
            return
        self.current_review_index += 1
        if self.current_review_index >= len(self.reviews):
            self.current_review_index = len(self.reviews) - 1
            self.log("✓ Все отзывы обработаны!")
            messagebox.showinfo("Готово", "Все отзывы обработаны!")
            return
        self.show_current_review()
        self.copy_review_btn.config(state=tk.NORMAL)
        self.paste_in_claude_btn.config(state=tk.DISABLED)
        self.copy_answer_btn.config(state=tk.DISABLED)
        self.paste_in_ozon_btn.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        self.log(f"→ Следующий отзыв #{self.current_review_index + 1}")

    def prev_review(self):
        """Переходит к предыдущему отзыву"""
        if not self.reviews:
            return
        self.current_review_index -= 1
        if self.current_review_index < 0:
            self.current_review_index = 0
        self.show_current_review()
        self.log(f"← Предыдущий отзыв #{self.current_review_index + 1}")

    def stop_automation(self):
        """Очищает интерфейс"""
        self.copy_review_btn.config(state=tk.DISABLED)
        self.paste_in_claude_btn.config(state=tk.DISABLED)
        self.copy_answer_btn.config(state=tk.DISABLED)
        self.paste_in_ozon_btn.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)

    def load_config(self):
        """Загружает конфигурацию"""
        pass


def main():
    root = tk.Tk()
    app = OzonReviewsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
