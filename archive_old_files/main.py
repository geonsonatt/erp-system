#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простая ERP система для курсовой работы
Главный модуль запуска системы с авторизацией
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import sys
import os

# Импортируем модули нашей ERP системы
from database import Database
from login_module import LoginWindow
from users_module import UsersModule
from products_module import ProductsModule
from customers_module import CustomersModule
from enhanced_orders_module import EnhancedOrdersModule
from reports_module import ReportsModule

class ERPMainWindow:
    def __init__(self, current_user):
        self.current_user = current_user
        self.root = tk.Tk()
        self.root.title(f"ERP Система - {current_user['full_name']} ({current_user['role']})")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Инициализируем базу данных
        self.db = Database()
        
        # Переменная для хранения текущего модуля
        self.current_module_frame = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Создаем главное меню
        self.create_menu()
        
        # Создаем панель пользователя
        self.create_user_panel()
        
        # Создаем заголовок
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🏢 ERP СИСТЕМА УПРАВЛЕНИЯ ПРЕДПРИЯТИЕМ", 
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Создаем фрейм для кнопок модулей
        buttons_frame = tk.Frame(self.root, bg='#f0f0f0')
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        # Создаем кнопки для модулей с учетом прав пользователя
        self.create_module_buttons(buttons_frame)
        
        # Создаем фрейм для содержимого модулей
        self.content_frame = tk.Frame(self.root, bg='white', relief='sunken', bd=2)
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Отображаем приветственное сообщение
        self.show_welcome_message()
        
    def create_user_panel(self):
        """Создать панель информации о пользователе"""
        user_frame = tk.Frame(self.root, bg='#34495e', height=40)
        user_frame.pack(fill='x')
        user_frame.pack_propagate(False)
        
        # Информация о пользователе
        user_info = tk.Label(
            user_frame,
            text=f"👤 {self.current_user['full_name']} | {self.current_user['role']} | {self.current_user['email']}",
            font=('Arial', 10),
            bg='#34495e',
            fg='white'
        )
        user_info.pack(side='left', padx=20, pady=10)
        
        # Кнопка выхода
        logout_btn = tk.Button(
            user_frame,
            text="🚪 Выйти",
            command=self.logout,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 9, 'bold'),
            relief='flat',
            cursor='hand2'
        )
        logout_btn.pack(side='right', padx=20, pady=5)
        
        # Время работы в системе
        import datetime
        current_time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
        time_label = tk.Label(
            user_frame,
            text=f"🕐 Время: {current_time}",
            font=('Arial', 9),
            bg='#34495e',
            fg='#bdc3c7'
        )
        time_label.pack(side='right', padx=20, pady=10)
        
    def create_module_buttons(self, parent):
        """Создать кнопки модулей с учетом прав доступа"""
        # Определяем доступные модули в зависимости от роли
        if self.current_user['role'] == 'Администратор':
            modules = [
                ("👥 Управление пользователями", self.open_users_module, '#3498db'),
                ("📦 Управление товарами", self.open_products_module, '#27ae60'),
                ("👤 Управление клиентами", self.open_customers_module, '#e67e22'),
                ("📋 Управление заказами", self.open_orders_module, '#9b59b6'),
                ("📊 Отчеты и аналитика", self.open_reports_module, '#34495e'),
                ("⚙️ Настройки системы", self.open_settings_module, '#95a5a6')
            ]
        elif self.current_user['role'] == 'Менеджер':
            modules = [
                ("📦 Управление товарами", self.open_products_module, '#27ae60'),
                ("👤 Управление клиентами", self.open_customers_module, '#e67e22'),
                ("📋 Управление заказами", self.open_orders_module, '#9b59b6'),
                ("📊 Отчеты и аналитика", self.open_reports_module, '#34495e')
            ]
        else:  # Оператор
            modules = [
                ("👤 Управление клиентами", self.open_customers_module, '#e67e22'),
                ("📋 Управление заказами", self.open_orders_module, '#9b59b6'),
                ("📊 Просмотр отчетов", self.open_reports_module, '#34495e')
            ]
        
        for i, (text, command, color) in enumerate(modules):
            btn = tk.Button(
                parent,
                text=text,
                command=command,
                font=('Arial', 12, 'bold'),
                bg=color,
                fg='white',
                relief='flat',
                cursor='hand2',
                width=25,
                height=2
            )
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=10, pady=5, sticky='ew')
            
        # Настраиваем сетку
        for i in range(3):
            parent.grid_columnconfigure(i, weight=1)
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="🏠 Главная", command=self.show_welcome_message)
        file_menu.add_separator()
        file_menu.add_command(label="💾 Резервная копия", command=self.create_backup)
        file_menu.add_command(label="📤 Экспорт данных", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Выход", command=self.logout)
        
        # Меню "Модули"
        modules_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Модули", menu=modules_menu)
        
        if self.current_user['role'] == 'Администратор':
            modules_menu.add_command(label="👥 Пользователи", command=self.open_users_module)
        if self.current_user['role'] in ['Администратор', 'Менеджер']:
            modules_menu.add_command(label="📦 Товары", command=self.open_products_module)
        modules_menu.add_command(label="👤 Клиенты", command=self.open_customers_module)
        modules_menu.add_command(label="📋 Заказы", command=self.open_orders_module)
        modules_menu.add_command(label="📊 Отчеты", command=self.open_reports_module)
        
        # Меню "Помощь"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="📖 Руководство пользователя", command=self.show_help)
        help_menu.add_command(label="🔍 Поиск", command=self.show_search)
        help_menu.add_separator()
        help_menu.add_command(label="ℹ️ О программе", command=self.show_about)
        
    def show_about(self):
        messagebox.showinfo(
            "О программе",
            f"ERP Система v2.0\n\nУлучшенная система управления предприятием\n\nТекущий пользователь: {self.current_user['full_name']}\nРоль: {self.current_user['role']}\n\nКурсовая работа\nРазработано на Python + Tkinter + SQLite"
        )
        
    def show_help(self):
        """Показать справку"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Руководство пользователя")
        help_window.geometry("600x400")
        help_window.configure(bg='white')
        
        help_text = tk.Text(help_window, wrap='word', font=('Arial', 10))
        help_text.pack(fill='both', expand=True, padx=20, pady=20)
        
        help_content = """
РУКОВОДСТВО ПОЛЬЗОВАТЕЛЯ ERP СИСТЕМЫ

1. ВХОД В СИСТЕМУ
   • Используйте ваш логин и пароль для входа
   • Доступные роли: Администратор, Менеджер, Оператор

2. НАВИГАЦИЯ
   • Главное меню - выбор модулей системы
   • Панель пользователя - информация о текущем пользователе
   • Кнопки модулей - быстрый доступ к функциям

3. МОДУЛИ СИСТЕМЫ

УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ (только Администратор):
   • Добавление новых пользователей
   • Просмотр списка пользователей
   • Удаление пользователей

УПРАВЛЕНИЕ ТОВАРАМИ (Администратор, Менеджер):
   • Добавление товаров в каталог
   • Редактирование информации о товарах
   • Контроль остатков на складе

УПРАВЛЕНИЕ КЛИЕНТАМИ:
   • Ведение базы клиентов
   • Добавление контактной информации
   • Просмотр истории взаимодействий

УПРАВЛЕНИЕ ЗАКАЗАМИ:
   • Создание новых заказов
   • Отслеживание статусов
   • Управление позициями заказов

ОТЧЕТЫ И АНАЛИТИКА:
   • Статистические отчеты
   • Аналитика продаж
   • Экспорт данных

4. ГОРЯЧИЕ КЛАВИШИ
   • F5 - Обновить данные
   • Ctrl+N - Добавить новую запись
   • Delete - Удалить выбранную запись
   • Ctrl+F - Поиск

5. БЕЗОПАСНОСТЬ
   • Регулярно меняйте пароли
   • Выходите из системы после работы
   • Создавайте резервные копии данных
        """
        
        help_text.insert('1.0', help_content)
        help_text.config(state='disabled')
        
    def show_search(self):
        """Глобальный поиск по системе"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Поиск по системе")
        search_window.geometry("500x400")
        search_window.configure(bg='white')
        
        # Поле поиска
        search_frame = tk.Frame(search_window, bg='white')
        search_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(search_frame, text="Поиск:", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w')
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, font=('Arial', 11), width=40)
        search_entry.pack(fill='x', pady=5)
        
        # Результаты поиска
        results_frame = tk.Frame(search_window, bg='white')
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(results_frame, text="Результаты поиска:", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w')
        
        results_tree = ttk.Treeview(results_frame, columns=('Тип', 'Название', 'Описание'), show='headings')
        results_tree.heading('Тип', text='Тип')
        results_tree.heading('Название', text='Название')
        results_tree.heading('Описание', text='Описание')
        results_tree.pack(fill='both', expand=True, pady=5)
        
        def perform_search():
            query = search_var.get().strip().lower()
            if not query:
                return
                
            # Очищаем результаты
            for item in results_tree.get_children():
                results_tree.delete(item)
                
            # Поиск в товарах
            products = self.db.get_all_products()
            for product in products:
                if query in product[1].lower() or query in (product[2] or '').lower():
                    results_tree.insert('', 'end', values=('Товар', product[1], product[2]))
                    
            # Поиск в клиентах
            customers = self.db.get_all_customers()
            for customer in customers:
                if query in customer[1].lower():
                    results_tree.insert('', 'end', values=('Клиент', customer[1], customer[2]))
                    
        search_btn = tk.Button(
            search_frame,
            text="🔍 Найти",
            command=perform_search,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        search_btn.pack(pady=5)
        
        search_entry.bind('<Return>', lambda e: perform_search())
        
    def create_backup(self):
        """Создать резервную копию базы данных"""
        import shutil
        import datetime
        
        try:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"erp_backup_{timestamp}.db"
            shutil.copy2("erp_database.db", backup_name)
            messagebox.showinfo("Успех", f"Резервная копия создана: {backup_name}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать резервную копию: {e}")
            
    def export_data(self):
        """Экспорт данных в CSV"""
        try:
            import csv
            import datetime
            
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Экспорт товаров
            with open(f'products_export_{timestamp}.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Название', 'Описание', 'Цена', 'Количество', 'Категория'])
                products = self.db.get_all_products()
                for product in products:
                    writer.writerow(product[:-1])  # Исключаем дату создания
                    
            messagebox.showinfo("Успех", f"Данные экспортированы в файл products_export_{timestamp}.csv")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {e}")
        
    def show_welcome_message(self):
        self.clear_content_frame()
        
        welcome_frame = tk.Frame(self.content_frame, bg='white')
        welcome_frame.pack(fill='both', expand=True)
        
        # Приветствие
        welcome_label = tk.Label(
            welcome_frame,
            text=f"Добро пожаловать в ERP систему, {self.current_user['full_name']}!",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        welcome_label.pack(pady=30)
        
        # Информация о роли
        role_info = {
            'Администратор': "У вас есть полный доступ ко всем модулям системы",
            'Менеджер': "У вас есть доступ к управлению товарами, клиентами и заказами",
            'Оператор': "У вас есть доступ к работе с клиентами и заказами"
        }
        
        role_label = tk.Label(
            welcome_frame,
            text=f"Ваша роль: {self.current_user['role']}\n{role_info[self.current_user['role']]}",
            font=('Arial', 12),
            bg='white',
            fg='#7f8c8d',
            justify='center'
        )
        role_label.pack(pady=10)
        
        # Быстрая статистика
        stats_frame = tk.Frame(welcome_frame, bg='white')
        stats_frame.pack(pady=30)
        
        tk.Label(
            stats_frame,
            text="📊 Быстрая статистика:",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=10)
        
        stats_text = f"""
💰 Общая сумма продаж: {self.db.get_total_sales():.2f} ₽
📦 Товаров в каталоге: {self.db.get_total_products()}
👥 Клиентов в базе: {self.db.get_total_customers()}
📋 Всего заказов: {self.db.get_total_orders()}
        """
        
        tk.Label(
            stats_frame,
            text=stats_text,
            font=('Arial', 11),
            bg='white',
            fg='#34495e',
            justify='left'
        ).pack()
        
    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def open_users_module(self):
        if self.current_user['role'] != 'Администратор':
            messagebox.showwarning("Доступ запрещен", "У вас нет прав для доступа к этому модулю!")
            return
        self.clear_content_frame()
        self.current_module = UsersModule(self.content_frame, self.db)
        
    def open_products_module(self):
        if self.current_user['role'] not in ['Администратор', 'Менеджер']:
            messagebox.showwarning("Доступ запрещен", "У вас нет прав для доступа к этому модулю!")
            return
        self.clear_content_frame()
        self.current_module = ProductsModule(self.content_frame, self.db)
        
    def open_customers_module(self):
        self.clear_content_frame()
        self.current_module = CustomersModule(self.content_frame, self.db)
        
    def open_orders_module(self):
        self.clear_content_frame()
        self.current_module = EnhancedOrdersModule(self.content_frame, self.db)
        
    def open_reports_module(self):
        self.clear_content_frame()
        self.current_module = ReportsModule(self.content_frame, self.db)
        
    def open_settings_module(self):
        if self.current_user['role'] != 'Администратор':
            messagebox.showwarning("Доступ запрещен", "У вас нет прав для доступа к настройкам!")
            return
        messagebox.showinfo("В разработке", "Модуль настроек находится в разработке")
        
    def logout(self):
        """Выход из системы"""
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти из системы?"):
            self.root.destroy()
            
    def run(self):
        self.root.mainloop()

def start_application(current_user):
    """Запуск главного приложения после авторизации"""
    app = ERPMainWindow(current_user)
    app.run()

def main():
    try:
        # Инициализируем базу данных
        db = Database()
        
        # Запускаем окно авторизации
        login_window = LoginWindow(db, start_application)
        user = login_window.run()
        
        # Если пользователь не авторизовался, завершаем программу
        if not user:
            sys.exit()
            
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка запуска программы: {e}")
        
if __name__ == "__main__":
    main() 