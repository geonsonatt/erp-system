# -*- coding: utf-8 -*-
"""
Модуль отчетов и аналитики ERP системы
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class ReportsModule:
    def __init__(self, parent_frame, database):
        self.parent = parent_frame
        self.db = database
        self.create_widgets()
        self.update_statistics()
        
    def create_widgets(self):
        # Заголовок модуля
        title_label = tk.Label(
            self.parent,
            text="ОТЧЕТЫ И АНАЛИТИКА",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Фрейм для статистических карточек
        stats_frame = tk.Frame(self.parent, bg='white')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Создаем статистические карточки
        self.create_stat_cards(stats_frame)
        
        # Фрейм для кнопок отчетов
        reports_frame = tk.Frame(self.parent, bg='white')
        reports_frame.pack(fill='x', padx=20, pady=10)
        
        reports_label = tk.Label(
            reports_frame,
            text="Доступные отчеты:",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        reports_label.pack(anchor='w', pady=(0, 10))
        
        # Кнопки отчетов
        reports_buttons_frame = tk.Frame(reports_frame, bg='white')
        reports_buttons_frame.pack(fill='x')
        
        reports = [
            ("📊 Общая сводка", self.show_general_summary, '#34495e'),
            ("👥 Отчет по пользователям", self.show_users_report, '#3498db'),
            ("📦 Отчет по товарам", self.show_products_report, '#27ae60'),
            ("👤 Отчет по клиентам", self.show_customers_report, '#e67e22'),
            ("📋 Отчет по заказам", self.show_orders_report, '#9b59b6'),
            ("📈 Графическая аналитика", self.show_analytics, '#1abc9c'),
            ("🔄 Обновить статистику", self.update_statistics, '#95a5a6')
        ]
        
        for i, (text, command, color) in enumerate(reports):
            btn = tk.Button(
                reports_buttons_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=('Arial', 10, 'bold'),
                relief='flat',
                cursor='hand2',
                width=25,
                height=2
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=5, sticky='ew')
            
        # Настраиваем сетку
        reports_buttons_frame.grid_columnconfigure(0, weight=1)
        reports_buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Фрейм для отображения отчетов
        self.report_frame = tk.Frame(self.parent, bg='white', relief='sunken', bd=2)
        self.report_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Показываем общую сводку по умолчанию
        self.show_general_summary()
        
    def create_stat_cards(self, parent):
        """Создание карточек со статистикой"""
        # Получаем статистику
        total_sales = self.db.get_total_sales()
        total_products = self.db.get_total_products()
        total_customers = self.db.get_total_customers()
        total_orders = self.db.get_total_orders()
        
        stats = [
            ("💰 Общая сумма продаж", f"{total_sales:.2f} ₽", '#27ae60'),
            ("📦 Количество товаров", str(total_products), '#3498db'),
            ("👥 Количество клиентов", str(total_customers), '#e67e22'),
            ("📋 Количество заказов", str(total_orders), '#9b59b6')
        ]
        
        for i, (title, value, color) in enumerate(stats):
            card = tk.Frame(parent, bg=color, relief='raised', bd=2)
            card.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            
            title_label = tk.Label(
                card,
                text=title,
                font=('Arial', 10, 'bold'),
                bg=color,
                fg='white'
            )
            title_label.pack(pady=(10, 5))
            
            value_label = tk.Label(
                card,
                text=value,
                font=('Arial', 14, 'bold'),
                bg=color,
                fg='white'
            )
            value_label.pack(pady=(0, 10))
            
        # Настраиваем колонки
        for i in range(4):
            parent.grid_columnconfigure(i, weight=1)
            
    def clear_report_frame(self):
        """Очистить фрейм отчетов"""
        for widget in self.report_frame.winfo_children():
            widget.destroy()
            
    def update_statistics(self):
        """Обновить статистику"""
        # Пересоздаем статистические карточки
        for widget in self.parent.winfo_children():
            if isinstance(widget, tk.Frame):
                # Ищем фрейм со статистикой
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame) and child.winfo_children():
                        # Проверяем, содержит ли карточки
                        first_child = child.winfo_children()[0]
                        if isinstance(first_child, tk.Frame):
                            # Удаляем старые карточки
                            for card in child.winfo_children():
                                card.destroy()
                            # Создаем новые
                            self.create_stat_cards(child)
                            break
        
        messagebox.showinfo("Обновлено", "Статистика успешно обновлена!")
        
    def show_general_summary(self):
        """Показать общую сводку"""
        self.clear_report_frame()
        
        # Заголовок отчета
        title_label = tk.Label(
            self.report_frame,
            text="ОБЩАЯ СВОДКА СИСТЕМЫ",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Текст сводки
        summary_text = tk.Text(
            self.report_frame,
            height=15,
            font=('Arial', 10),
            bg='#f8f9fa',
            relief='flat',
            wrap='word'
        )
        summary_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Формируем содержимое сводки
        total_sales = self.db.get_total_sales()
        total_products = self.db.get_total_products()
        total_customers = self.db.get_total_customers()
        total_orders = self.db.get_total_orders()
        
        current_date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        
        summary_content = f"""
ОТЧЕТ ПО СОСТОЯНИЮ ERP СИСТЕМЫ
Дата формирования: {current_date}

═══════════════════════════════════════════════════════════════

📈 КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ:

💰 Общая сумма продаж: {total_sales:.2f} ₽
📦 Товаров в каталоге: {total_products} шт.
👥 Клиентов в базе: {total_customers} чел.
📋 Всего заказов: {total_orders} шт.

═══════════════════════════════════════════════════════════════

📊 АНАЛИЗ:

• Средняя сумма заказа: {(total_sales / total_orders if total_orders > 0 else 0):.2f} ₽
• Заказов на клиента: {(total_orders / total_customers if total_customers > 0 else 0):.1f}

═══════════════════════════════════════════════════════════════

💡 РЕКОМЕНДАЦИИ:

1. Система работает стабильно
2. Для увеличения оборота рекомендуется:
   - Расширить каталог товаров
   - Провести маркетинговые мероприятия
   - Улучшить сервис обслуживания клиентов

3. Контроль качества:
   - Регулярно обновляйте информацию о товарах
   - Следите за статусами заказов
   - Поддерживайте связь с клиентами

═══════════════════════════════════════════════════════════════

Система ERP v1.0 - Курсовая работа
"""
        
        summary_text.insert('1.0', summary_content)
        summary_text.config(state='disabled')
        
    def show_users_report(self):
        """Показать отчет по пользователям"""
        self.clear_report_frame()
        
        title_label = tk.Label(
            self.report_frame,
            text="ОТЧЕТ ПО ПОЛЬЗОВАТЕЛЯМ",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Таблица пользователей
        columns = ('ID', 'Логин', 'Полное имя', 'Роль', 'Email')
        tree = ttk.Treeview(self.report_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
            
        # Загружаем данные
        users = self.db.get_all_users()
        for user in users:
            tree.insert('', 'end', values=(user[0], user[1], user[3], user[4], user[5]))
            
        tree.pack(fill='both', expand=True, padx=20, pady=10)
        
    def show_products_report(self):
        """Показать отчет по товарам"""
        self.clear_report_frame()
        
        title_label = tk.Label(
            self.report_frame,
            text="ОТЧЕТ ПО ТОВАРАМ",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Таблица товаров
        columns = ('ID', 'Название', 'Цена', 'Количество', 'Категория')
        tree = ttk.Treeview(self.report_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
            
        # Загружаем данные
        products = self.db.get_all_products()
        for product in products:
            tree.insert('', 'end', values=(
                product[0], product[1], f"{product[3]:.2f} ₽", 
                product[4], product[5]
            ))
            
        tree.pack(fill='both', expand=True, padx=20, pady=10)
        
    def show_customers_report(self):
        """Показать отчет по клиентам"""
        self.clear_report_frame()
        
        title_label = tk.Label(
            self.report_frame,
            text="ОТЧЕТ ПО КЛИЕНТАМ",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Таблица клиентов
        columns = ('ID', 'Название', 'Email', 'Телефон', 'Адрес')
        tree = ttk.Treeview(self.report_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)
            
        # Загружаем данные
        customers = self.db.get_all_customers()
        for customer in customers:
            tree.insert('', 'end', values=(
                customer[0], customer[1], customer[2], customer[3], customer[4]
            ))
            
        tree.pack(fill='both', expand=True, padx=20, pady=10)
        
    def show_orders_report(self):
        """Показать отчет по заказам"""
        self.clear_report_frame()
        
        title_label = tk.Label(
            self.report_frame,
            text="ОТЧЕТ ПО ЗАКАЗАМ",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Таблица заказов
        columns = ('№ Заказа', 'Клиент', 'Сумма', 'Статус', 'Дата')
        tree = ttk.Treeview(self.report_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
            
        # Загружаем данные
        orders = self.db.get_all_orders()
        for order in orders:
            tree.insert('', 'end', values=(
                f"#{order[0]:04d}", order[1], f"{order[2]:.2f} ₽", 
                order[3], order[4]
            ))
            
        tree.pack(fill='both', expand=True, padx=20, pady=10)
        
    def show_analytics(self):
        """Показать графическую аналитику"""
        self.clear_report_frame()
        
        try:
            from analytics_module import AnalyticsModule
            self.analytics = AnalyticsModule(self.report_frame, self.db)
        except ImportError:
            messagebox.showerror("Ошибка", "Модуль графической аналитики не найден!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить аналитику: {e}")
            
        # Показываем общую сводку системы по умолчанию
        self.show_general_summary() 