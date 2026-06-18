#!/usr/bin/env python3
"""
Ozon Reviews Auto Responder
Автоматизирует процесс ответов на отзывы на Ozon с помощью Claude API
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
        self.root.title("Ozon Reviews Auto Responder")
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
        self.start_btn = ttk.Button(left_frame, text="4. Начать автоматизацию", command=self.start_automation)
        self.start_btn.pack(fill=tk.X, pady=5)
        self.start_btn.config(state=tk.DISABLED)

        # Кнопка остановить
        self.stop_btn = ttk.Button(left_frame, text="⏹ Остановить", command=self.stop_automation)
        self.stop_btn.pack(fill=tk.X, pady=5)
        self.stop_btn.config(state=tk.DISABLED)

        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        # Настройки
        settings_label = ttk.Label(left_frame, text="Настройки", font=("Arial", 12, "bold"))
        settings_label.pack(pady=10)

        # API ключ Claude
        ttk.Label(left_frame, text="Claude API Key:").pack(anchor=tk.W, pady=(5, 0))
        self.api_key_entry = ttk.Entry(left_frame, width=25, show="*")
        self.api_key_entry.pack(fill=tk.X, pady=5)

        # Промежуток времени между ответами
        ttk.Label(left_frame, text="Задержка (сек):").pack(anchor=tk.W, pady=(5, 0))
        self.delay_spinbox = ttk.Spinbox(left_frame, from_=1, to=30, width=25)
        self.delay_spinbox.set(3)
        self.delay_spinbox.pack(fill=tk.X, pady=5)

        # Сохранить настройки
        self.save_config_btn = ttk.Button(left_frame, text="Сохранить", command=self.save_config)
        self.save_config_btn.pack(fill=tk.X, pady=5)

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

        # Лог
        log_frame = ttk.LabelFrame(right_frame, text="Лог операций", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=70, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Текущий отзыв
        review_frame = ttk.LabelFrame(right_frame, text="Текущий отзыв", padding=5)
        review_frame.pack(fill=tk.X, pady=5)

        self.current_review_text = scrolledtext.ScrolledText(review_frame, height=4, width=70, wrap=tk.WORD)
        self.current_review_text.pack(fill=tk.X)

        # Ответ от Claude
        answer_frame = ttk.LabelFrame(right_frame, text="Ответ от Claude", padding=5)
        answer_frame.pack(fill=tk.X, pady=5)

        self.current_answer_text = scrolledtext.ScrolledText(answer_frame, height=4, width=70, wrap=tk.WORD)
        self.current_answer_text.pack(fill=tk.X)

        # Кнопки управления текущим отзывом
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=5)

        self.approve_btn = ttk.Button(button_frame, text="✓ Одобрить и отправить", command=self.approve_current)
        self.approve_btn.pack(side=tk.LEFT, padx=5)
        self.approve_btn.config(state=tk.DISABLED)

        self.skip_btn = ttk.Button(button_frame, text="⊘ Пропустить", command=self.skip_current)
        self.skip_btn.pack(side=tk.LEFT, padx=5)
        self.skip_btn.config(state=tk.DISABLED)

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
            self.start_btn.config(state=tk.NORMAL)
        except Exception as e:
            self.log(f"✗ Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", str(e))

    def open_claude(self):
        """Открывает Claude"""
        self.log("Открываю Claude...")
        try:
            self.automation.open_claude()
            self.log("✓ Claude открыт")
        except Exception as e:
            self.log(f"✗ Ошибка: {str(e)}")

    def start_automation(self):
        """Начинает автоматизацию"""
        if not self.reviews:
            messagebox.showwarning("Предупреждение", "Сначала загрузите отзывы")
            return

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.load_reviews_btn.config(state=tk.DISABLED)

        # Запускаем в отдельном потоке
        thread = threading.Thread(target=self.automation_loop)
        thread.daemon = True
        thread.start()

    def automation_loop(self):
        """Основной цикл автоматизации"""
        try:
            for i, review in enumerate(self.reviews):
                if not self.is_running:
                    break

                self.current_review_index = i
                self.process_review(review, i)
                self.progress_label.config(text=f"Отзывы: {i+1}/{len(self.reviews)}")

            self.log("✓ Обработка завершена")
            self.status_label.config(text="Завершено", foreground="green")
            self.stop_automation()
        except Exception as e:
            self.log(f"✗ Ошибка в цикле: {str(e)}")
            self.stop_automation()

    def process_review(self, review, index):
        """Обрабатывает один отзыв"""
        try:
            self.status_label.config(text="Обработка...", foreground="blue")
            self.log(f"\n--- Отзыв #{index + 1} ---")
            self.log(f"Текст: {review.get('text', 'N/A')[:100]}...")

            # Показываем текущий отзыв
            self.current_review_text.delete(1.0, tk.END)
            self.current_review_text.insert(1.0, review.get('text', ''))

            # Копируем отзыв в буфер обмена
            self.automation.copy_to_clipboard(review.get('text', ''))
            self.log("Отзыв скопирован в буфер обмена")

            # Переключаемся на Claude и вставляем
            self.log("Переключаюсь на Claude...")
            self.automation.switch_to_claude()
            time.sleep(2)

            # Вставляем отзыв (Ctrl+V)
            self.automation.paste()
            self.log("Отзыв вставлен в Claude")

            # Ждем ответа
            self.log("Ожидаю ответ от Claude... (нажмите Enter в Claude)")
            self.log("⏳ Можно вручную нажать Enter и дождаться ответа")

            # Даем время на генерацию ответа
            delay = int(self.delay_spinbox.get())
            for remaining in range(delay, 0, -1):
                if not self.is_running:
                    return
                self.status_label.config(text=f"Ожидание... {remaining}с")
                time.sleep(1)

            # Копируем ответ (Ctrl+A, Ctrl+C)
            self.automation.select_all()
            time.sleep(0.5)
            self.automation.copy()
            answer = self.automation.read_clipboard()

            self.log(f"Ответ получен: {answer[:100]}...")
            self.current_answer_text.delete(1.0, tk.END)
            self.current_answer_text.insert(1.0, answer)

            # Переключаемся обратно на Ozon
            self.log("Переключаюсь на Ozon...")
            self.automation.switch_to_ozon()
            time.sleep(2)

            # Вставляем ответ в форму
            self.automation.paste()
            self.log("Ответ вставлен в форму Ozon")

            # Отправляем
            self.log("Отправляю ответ...")
            self.automation.send_answer()
            self.log("✓ Ответ отправлен успешно")
            self.status_label.config(text="Готово", foreground="green")

        except Exception as e:
            self.log(f"✗ Ошибка обработки: {str(e)}")
            self.status_label.config(text="Ошибка", foreground="red")

    def approve_current(self):
        """Одобрить текущий ответ"""
        self.log("✓ Ответ одобрен")
        self.approve_btn.config(state=tk.DISABLED)
        self.skip_btn.config(state=tk.DISABLED)

    def skip_current(self):
        """Пропустить текущий отзыв"""
        self.log("⊘ Отзыв пропущен")
        self.approve_btn.config(state=tk.DISABLED)
        self.skip_btn.config(state=tk.DISABLED)

    def stop_automation(self):
        """Останавливает автоматизацию"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.load_reviews_btn.config(state=tk.NORMAL)
        self.log("Обработка остановлена")

    def save_config(self):
        """Сохраняет конфигурацию"""
        api_key = self.api_key_entry.get()
        delay = self.delay_spinbox.get()

        if not api_key:
            messagebox.showwarning("Предупреждение", "Введите API ключ Claude")
            return

        self.config.set_api_key(api_key)
        self.config.set_delay(int(delay))
        self.automation.set_api_key(api_key)
        self.log("✓ Настройки сохранены")
        messagebox.showinfo("Успех", "Настройки сохранены")

    def load_config(self):
        """Загружает конфигурацию"""
        api_key = self.config.get_api_key()
        delay = self.config.get_delay()

        if api_key:
            self.api_key_entry.insert(0, api_key)
        self.delay_spinbox.set(delay)


def main():
    root = tk.Tk()
    app = OzonReviewsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
