#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полнофункциональная ERP система v3.0 на Tkinter с базой данных SQLite.
Реализованы CRUD-операции для пользователей, товаров, клиентов и заказов.
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3
from datetime import datetime

DB_NAME = 'erp_database.db'


class Database:
    """Класс для работы с базой данных SQLite: инициализация и основные операции."""

    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.conn = None
        self.init_database()

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def init_database(self):
        """Создает соединение и таблицы, если они не существуют."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            # Создание таблицы пользователей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    email TEXT UNIQUE,
                    password TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            # Создание таблицы продуктов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL DEFAULT 0,
                    quantity INTEGER NOT NULL DEFAULT 0,
                    category TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            # Создание таблицы клиентов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    address TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            # Создание таблицы заказов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    total_amount REAL NOT NULL DEFAULT 0,
                    status TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    FOREIGN KEY(customer_id) REFERENCES customers(id)
                )
            """)
            # Создание таблицы пунктов заказа (OrderItems)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 1,
                    price REAL NOT NULL DEFAULT 0,
                    FOREIGN KEY(order_id) REFERENCES orders(id),
                    FOREIGN KEY(product_id) REFERENCES products(id)
                )
            """)
            conn.commit()
            # Если база пуста - создадим администратора по умолчанию
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""
                    INSERT INTO users (username, full_name, role, email, password, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, ("admin", "Администратор Системы", "Администратор", "admin@example.com", "admin123", now))
                conn.commit()
        except Exception as e:
            print(f"❌ Ошибка инициализации БД: {e}")

    def fetch_all(self, table, order_by=None):
        """Возвращает все записи из таблицы."""
        try:
            cursor = self.connect().cursor()
            query = f"SELECT * FROM {table}"
            if order_by:
                query += f" ORDER BY {order_by}"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось получить данные из {table}: {e}")
            return []

    def insert(self, table, columns, values):
        """Вставляет запись в таблицу. columns и values — списки одинаковой длины."""
        try:
            cursor = self.connect().cursor()
            cols = ", ".join(columns)
            placeholders = ", ".join("?" for _ in values)
            query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
            cursor.execute(query, values)
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось добавить запись в {table}: {e}")
            return None

    def update(self, table, record_id, columns, values):
        """Обновляет запись по id. columns и values — списки одинаковой длины."""
        try:
            cursor = self.connect().cursor()
            set_clause = ", ".join(f"{col}=?" for col in columns)
            query = f"UPDATE {table} SET {set_clause} WHERE id=?"
            cursor.execute(query, values + [record_id])
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось обновить запись в {table}: {e}")

    def delete(self, table, record_id):
        """Удаляет запись по id."""
        try:
            cursor = self.connect().cursor()
            query = f"DELETE FROM {table} WHERE id=?"
            cursor.execute(query, (record_id,))
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось удалить запись из {table}: {e}")


class SimpleERP:
    """Основной класс ERP приложения: создает интерфейс и связывает его с БД."""

    def __init__(self):
        self.db = Database()
        self.root = tk.Tk()
        self.root.title("💼 ERP Система v3.0")
        self.root.geometry("900x650")
        self.root.configure(bg='#f0f0f0')

        # Текущий пользователь (по умолчанию admin)
        self.current_user = self.get_default_user()

        # Создаем интерфейс
        self.create_interface()

    def get_default_user(self):
        """Загружает первую запись пользователя (admin) при старте."""
        users = self.db.fetch_all('users', order_by="id LIMIT 1")
        if users:
            uid, username, full_name, role, email, _, _ = users[0]
            return {
                'id': uid,
                'username': username,
                'full_name': full_name,
                'role': role,
                'email': email
            }
        return {
            'id': None, 'username': 'guest', 'full_name': 'Гость', 'role': 'Гость', 'email': ''
        }

    def create_interface(self):
        """Создание графического интерфейса приложения."""

        # Шапка
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        title_label = tk.Label(
            header_frame,
            text="🏢 ERP СИСТЕМА УПРАВЛЕНИЯ ПРЕДПРИЯТИЕМ v3.0",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(expand=True)

        # Информация о пользователе и времени
        user_frame = tk.Frame(self.root, bg='#34495e', height=40)
        user_frame.pack(fill='x')
        user_frame.pack_propagate(False)
        self.user_info_label = tk.Label(
            user_frame,
            text="",
            font=('Arial', 10),
            bg='#34495e',
            fg='white'
        )
        self.user_info_label.pack(pady=8)
        self.update_user_info()

        # Панель кнопок модулей
        buttons_frame = tk.Frame(self.root, bg='#f0f0f0')
        buttons_frame.pack(fill='x', padx=20, pady=15)
        modules = [
            ("👥 Пользователи", self.show_users, '#3498db'),
            ("📦 Товары", self.show_products, '#27ae60'),
            ("👤 Клиенты", self.show_customers, '#e67e22'),
            ("📋 Заказы", self.show_orders, '#9b59b6'),
            ("📊 Статистика", self.show_stats, '#34495e'),
            ("❌ Выход", self.exit_app, '#e74c3c')
        ]
        for i, (text, command, color) in enumerate(modules):
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                font=('Arial', 11, 'bold'),
                bg=color,
                fg='white',
                relief='flat',
                width=14,
                height=2
            )
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=8, pady=5, sticky='ew')
            buttons_frame.grid_columnconfigure(col, weight=1)

        # Основная область для отображения модулей
        self.content_frame = tk.Frame(self.root, bg='white', relief='sunken', bd=2)
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        self.show_welcome()

    def update_user_info(self):
        """Обновление информации о пользователе и текущего времени."""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text = f"👤 {self.current_user['full_name']} | {self.current_user['role']} | Время: {now}"
        self.user_info_label.config(text=text)
        # Обновляем каждые 1 секунду
        self.root.after(1000, self.update_user_info)

    def clear_content(self):
        """Удаляет все виджеты из content_frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_welcome(self):
        """Отображение приветственного экрана с базовой статистикой."""
        self.clear_content()
        welcome_label = tk.Label(
            self.content_frame,
            text=f"Добро пожаловать в ERP систему, {self.current_user['full_name']}!",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        welcome_label.pack(pady=40)

        # Быстрая статистика
        stats = {}
        stats['users'] = len(self.db.fetch_all('users'))
        stats['products'] = len(self.db.fetch_all('products'))
        stats['customers'] = len(self.db.fetch_all('customers'))
        stats['orders'] = len(self.db.fetch_all('orders'))
        cursor = self.db.connect().cursor()
        cursor.execute("SELECT SUM(total_amount) FROM orders")
        stats['total_sales'] = cursor.fetchone()[0] or 0

        stats_text = (
            f"📊 СОСТОЯНИЕ СИСТЕМЫ:\n\n"
            f"👥 Пользователей: {stats['users']}\n"
            f"📦 Товаров: {stats['products']}\n"
            f"👤 Клиентов: {stats['customers']}\n"
            f"📋 Заказов: {stats['orders']}\n"
            f"💰 Общая сумма продаж: {stats['total_sales']:.2f} ₽\n\n"
            "🎯 Система готова к работе!"
        )
        stats_label = tk.Label(
            self.content_frame,
            text=stats_text,
            font=('Arial', 13),
            bg='white',
            fg='#34495e',
            justify='left'
        )
        stats_label.pack(pady=20)

    # ------------------ МОДУЛЬ: УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ ------------------

    def show_users(self):
        """Отображает интерфейс для управления пользователями."""
        self.clear_content()
        title = tk.Label(
            self.content_frame,
            text="👥 УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#3498db'
        )
        title.pack(pady=15)

        # Панель кнопок CRUD
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=(0, 10))
        tk.Button(btn_frame, text="Добавить", command=self.add_user, bg='#2ecc71', fg='white',
                  font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_user, bg='#f1c40f', fg='white',
                  font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_user, bg='#e74c3c', fg='white',
                  font=('Arial', 11, 'bold')).pack(side='left', padx=5)

        # Таблица пользователей
        columns = ('id', 'username', 'full_name', 'role', 'email', 'created_at')
        self.users_tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', selectmode='browse')
        headings = {
            'id': 'ID', 'username': 'Логин', 'full_name': 'Полное имя',
            'role': 'Роль', 'email': 'Email', 'created_at': 'Дата создания'
        }
        for col in columns:
            self.users_tree.heading(col, text=headings[col])
            self.users_tree.column(col, width=100, anchor='center')
        self.users_tree.column('username', width=120)
        self.users_tree.column('full_name', width=180)
        self.users_tree.column('email', width=180)
        self.users_tree.pack(fill='both', expand=True, padx=20, pady=10)

        self.load_users()

    def load_users(self):
        """Загружает список пользователей в таблицу."""
        for row in self.users_tree.get_children():
            self.users_tree.delete(row)
        users = self.db.fetch_all('users', order_by='id')
        for user in users:
            self.users_tree.insert('', 'end', values=user)

    def add_user(self):
        """Окно для добавления нового пользователя."""
        dialog = UserForm(self.root, "Добавить пользователя")
        if dialog.result:
            username, full_name, role, email, password = dialog.result
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.insert('users',
                           ['username', 'full_name', 'role', 'email', 'password', 'created_at'],
                           [username, full_name, role, email, password, now])
            self.load_users()

    def edit_user(self):
        """Редактирует выбранного пользователя."""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Выбор пользователя", "Пожалуйста, выберите пользователя для редактирования.")
            return
        values = self.users_tree.item(selected[0], 'values')
        user_id = values[0]
        dialog = UserForm(self.root, "Редактировать пользователя", initial=values[1:])
        if dialog.result:
            username, full_name, role, email, password = dialog.result
            self.db.update('users', user_id,
                           ['username', 'full_name', 'role', 'email', 'password'],
                           [username, full_name, role, email, password])
            self.load_users()

    def delete_user(self):
        """Удаляет выбранного пользователя после подтверждения."""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Выбор пользователя", "Пожалуйста, выберите пользователя для удаления.")
            return
        values = self.users_tree.item(selected[0], 'values')
        user_id, username = values[0], values[1]
        if messagebox.askyesno("Удалить пользователя", f"Удалить пользователя '{username}'?"):
            self.db.delete('users', user_id)
            self.load_users()

    # ------------------ МОДУЛЬ: УПРАВЛЕНИЕ ТОВАРАМИ ------------------

    def show_products(self):
        """Отображает интерфейс для управления товарами."""
        self.clear_content()
        title = tk.Label(
            self.content_frame,
            text="📦 УПРАВЛЕНИЕ ТОВАРАМИ",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#27ae60'
        )
        title.pack(pady=15)

        # Панель кнопок CRUD
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=(0, 10))
        tk.Button(btn_frame, text="Добавить", command=self.add_product, bg='#2ecc71', fg='white',
                  font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_product, bg='#f1c40f', fg='white',
                  font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_product, bg='#e74c3c', fg='white',
                  font=('Arial', 11, 'bold')).pack(side='left', padx=5)

        # Таблица товаров
        columns = ('id', 'name', 'price', 'quantity', 'category', 'created_at')
        self.products_tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', selectmode='browse')
        headings = {
            'id': 'ID', 'name': 'Название', 'price': 'Цена (₽)',
            'quantity': 'Остаток', 'category': 'Категория', 'created_at': 'Дата создания'
        }
        for col in columns:
            self.products_tree.heading(col, text=headings[col])
            self.products_tree.column(col, width=100, anchor='center')
        self.products_tree.column('name', width=180)
        self.products_tree.column('category', width=120)
        self.products_tree.pack(fill='both', expand=True, padx=20, pady=10)

        self.load_products()

    def load_products(self):
        """Загружает список товаров в таблицу."""
        for row in self.products_tree.get_children():
            self.products_tree.delete(row)
        products = self.db.fetch_all('products', order_by='name')
        for prod in products:
            pid, name, price, qty, category, created = prod
            self.products_tree.insert('', 'end', values=(pid, name, f"{price:.2f}", qty, category, created))

    def add_product(self):
        """Окно для добавления нового товара."""
        dialog = ProductForm(self.root, "Добавить товар")
        if dialog.result:
            name, price, quantity, category = dialog.result
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.insert('products',
                           ['name', 'price', 'quantity', 'category', 'created_at'],
                           [name, price, quantity, category, now])
            self.load_products()

    def edit_product(self):
        """Редактирует выбранный товар."""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Выбор товара", "Пожалуйста, выберите товар для редактирования.")
            return
        values = self.products_tree.item(selected[0], 'values')
        product_id = values[0]
        # Приводим price к float, quantity к int
        initial = (values[1], float(values[2]), int(values[3]), values[4])
        dialog = ProductForm(self.root, "Редактировать товар", initial=initial)
        if dialog.result:
            name, price, quantity, category = dialog.result
            self.db.update('products', product_id,
                           ['name', 'price', 'quantity', 'category'],
                           [name, price, quantity, category])
            self.load_products()

    def delete_product(self):
        """Удаляет выбранный товар после подтверждения."""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Выбор товара", "Пожалуйста, выберите товар для удаления.")
            return
        values = self.products_tree.item(selected[0], 'values')
        product_id, name = values[0], values[1]
        if messagebox.askyesno("Удалить товар", f"Удалить товар '{name}'?"):
            self.db.delete('products', product_id)
            self.load_products()

    # ------------------ МОДУЛЬ: УПРАВЛЕНИЕ КЛИЕНТАМИ ------------------

    def show_customers(self):
        """Отображает интерфейс для управления клиентами."""
        self.clear_content()
        title = tk.Label(
            self.content_frame,
            text="👤 УПРАВЛЕНИЕ КЛИЕНТАМИ",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#e67e22'
        )
        title.pack(pady=15)

        # Панель кнопок CRUD
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=(0, 10))
        tk.Button(btn_frame, text="Добавить", command=self.add_customer, bg='#2ecc71', fg='white',
                  font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_customer, bg='#f1c40f', fg='white',
                  font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_customer, bg='#e74c3c', fg='white',
                  font=('Arial', 11, 'bold')).pack(side='left', padx=5)

        # Таблица клиентов
        columns = ('id', 'name', 'email', 'phone', 'address', 'created_at')
        self.customers_tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', selectmode='browse')
        headings = {
            'id': 'ID', 'name': 'Имя/Компания', 'email': 'Email',
            'phone': 'Телефон', 'address': 'Адрес', 'created_at': 'Дата создания'
        }
        for col in columns:
            self.customers_tree.heading(col, text=headings[col])
            self.customers_tree.column(col, width=100, anchor='center')
        self.customers_tree.column('name', width=180)
        self.customers_tree.column('email', width=180)
        self.customers_tree.pack(fill='both', expand=True, padx=20, pady=10)

        self.load_customers()

    def load_customers(self):
        """Загружает список клиентов в таблицу."""
        for row in self.customers_tree.get_children():
            self.customers_tree.delete(row)
        customers = self.db.fetch_all('customers', order_by='name')
        for cust in customers:
            cid, name, email, phone, address, created = cust
            self.customers_tree.insert('', 'end', values=(cid, name, email, phone, address, created))

    def add_customer(self):
        """Окно для добавления нового клиента."""
        dialog = CustomerForm(self.root, "Добавить клиента")
        if dialog.result:
            name, email, phone, address = dialog.result
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.insert('customers',
                           ['name', 'email', 'phone', 'address', 'created_at'],
                           [name, email, phone, address, now])
            self.load_customers()

    def edit_customer(self):
        """Редактирует выбранного клиента."""
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showwarning("Выбор клиента", "Пожалуйста, выберите клиента для редактирования.")
            return
        values = self.customers_tree.item(selected[0], 'values')
        cust_id = values[0]
        initial = (values[1], values[2], values[3], values[4])
        dialog = CustomerForm(self.root, "Редактировать клиента", initial=initial)
        if dialog.result:
            name, email, phone, address = dialog.result
            self.db.update('customers', cust_id,
                           ['name', 'email', 'phone', 'address'],
                           [name, email, phone, address])
            self.load_customers()

    def delete_customer(self):
        """Удаляет выбранного клиента после подтверждения."""
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showwarning("Выбор клиента", "Пожалуйста, выберите клиента для удаления.")
            return
        values = self.customers_tree.item(selected[0], 'values')
        cust_id, name = values[0], values[1]
        if messagebox.askyesno("Удалить клиента", f"Удалить клиента '{name}'?"):
            self.db.delete('customers', cust_id)
            self.load_customers()

    # ------------------ МОДУЛЬ: УПРАВЛЕНИЕ ЗАКАЗАМИ ------------------

    def show_orders(self):
        """Отображает интерфейс для управления заказами."""
        self.clear_content()
        title = tk.Label(
            self.content_frame,
            text="📋 УПРАВЛЕНИЕ ЗАКАЗАМИ",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#9b59b6'
        )
        title.pack(pady=15)

        # Панель кнопок CRUD и добавления позиций
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=(0, 10))
        tk.Button(btn_frame, text="Добавить заказ", command=self.add_order, bg='#2ecc71', fg='white',
                  font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Изменить статус", command=self.change_order_status, bg='#f1c40f', fg='white',
                  font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить заказ", command=self.delete_order, bg='#e74c3c', fg='white',
                  font=('Arial', 11, 'bold')).pack(side='left', padx=5)

        # Таблица заказов
        columns = ('id', 'customer', 'total_amount', 'status', 'created_date')
        self.orders_tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', selectmode='browse')
        headings = {
            'id': '№ заказа', 'customer': 'Клиент', 'total_amount': 'Сумма (₽)',
            'status': 'Статус', 'created_date': 'Дата создания'
        }
        for col in columns:
            self.orders_tree.heading(col, text=headings[col])
            self.orders_tree.column(col, width=100, anchor='center')
        self.orders_tree.column('customer', width=180)
        self.orders_tree.pack(fill='both', expand=True, padx=20, pady=10)

        self.load_orders()

    def load_orders(self):
        """Загружает список заказов в таблицу."""
        for row in self.orders_tree.get_children():
            self.orders_tree.delete(row)
        cursor = self.db.connect().cursor()
        cursor.execute("""
            SELECT o.id, c.name, o.total_amount, o.status, o.created_date
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            ORDER BY o.created_date DESC
        """)
        for order in cursor.fetchall():
            oid, cust_name, total, status, created = order
            self.orders_tree.insert('', 'end', values=(f"#{oid:04d}", cust_name, f"{total:.2f}", status, created))

    def add_order(self):
        """Окно для создания нового заказа с добавлением позиций."""
        dialog = OrderForm(self.root, self.db)
        if dialog.result:
            customer_id, items = dialog.result
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total_amount = sum(item['quantity'] * item['price'] for item in items)
            status = "Новый"
            order_id = self.db.insert('orders',
                                      ['customer_id', 'total_amount', 'status', 'created_date'],
                                      [customer_id, total_amount, status, now])
            # Добавляем позиции в order_items
            for item in items:
                self.db.insert('order_items',
                               ['order_id', 'product_id', 'quantity', 'price'],
                               [order_id, item['product_id'], item['quantity'], item['price']])
                # Уменьшаем количество товара на складе
                cursor = self.db.connect().cursor()
                cursor.execute("SELECT quantity FROM products WHERE id=?", (item['product_id'],))
                current_qty = cursor.fetchone()[0]
                new_qty = current_qty - item['quantity']
                self.db.update('products', item['product_id'], ['quantity'], [new_qty])
            self.load_orders()
            self.load_products()  # чтобы отобразить обновленный остаток

    def change_order_status(self):
        """Изменяет статус выбранного заказа."""
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Выбор заказа", "Пожалуйста, выберите заказ для изменения статуса.")
            return
        values = self.orders_tree.item(selected[0], 'values')
        order_number = values[0]  # вида "#0001"
        order_id = int(order_number.strip('#'))
        # Диалог выбора нового статуса
        new_status = simpledialog.askstring("Статус заказа", "Введите новый статус:", parent=self.root)
        if new_status:
            cursor = self.db.connect().cursor()
            cursor.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))
            self.db.conn.commit()
            self.load_orders()

    def delete_order(self):
        """Удаляет выбранный заказ после подтверждения и восстанавливает остаток товаров."""
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Выбор заказа", "Пожалуйста, выберите заказ для удаления.")
            return
        values = self.orders_tree.item(selected[0], 'values')
        order_number = values[0]
        order_id = int(order_number.strip('#'))
        if messagebox.askyesno("Удалить заказ", f"Удалить заказ {order_number}?"):
            # Перед удалением восстанавливаем остаток товаров
            cursor = self.db.connect().cursor()
            cursor.execute("SELECT product_id, quantity FROM order_items WHERE order_id=?", (order_id,))
            items = cursor.fetchall()
            for prod_id, qty in items:
                cursor.execute("SELECT quantity FROM products WHERE id=?", (prod_id,))
                current_qty = cursor.fetchone()[0]
                new_qty = current_qty + qty
                self.db.update('products', prod_id, ['quantity'], [new_qty])
            # Удаляем позиции заказа
            self.db.delete('order_items', order_id)  # удалим все order_items (чтобы заработал ON DELETE CASCADE, но не во всех SQLite версиях)
            cursor.execute("DELETE FROM order_items WHERE order_id=?", (order_id,))
            self.db.conn.commit()
            # Удаляем сам заказ
            self.db.delete('orders', order_id)
            self.load_orders()
            self.load_products()

    # ------------------ МОДУЛЬ: СТАТИСТИКА И АНАЛИТИКА ------------------

    def show_stats(self):
        """Отображает подробную статистику работы системы."""
        self.clear_content()
        title = tk.Label(
            self.content_frame,
            text="📊 СТАТИСТИКА И АНАЛИТИКА",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#34495e'
        )
        title.pack(pady=15)

        cursor = self.db.connect().cursor()
        stats = {}

        # Пользователи
        cursor.execute("SELECT COUNT(*) FROM users")
        stats['users'] = cursor.fetchone()[0]

        # Товары и остаток
        cursor.execute("SELECT COUNT(*) FROM products")
        stats['products'] = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(quantity) FROM products")
        stats['total_products_qty'] = cursor.fetchone()[0] or 0

        # Клиенты
        cursor.execute("SELECT COUNT(*) FROM customers")
        stats['customers'] = cursor.fetchone()[0]

        # Заказы и суммы
        cursor.execute("SELECT COUNT(*) FROM orders")
        stats['orders'] = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(total_amount) FROM orders")
        stats['total_sales'] = cursor.fetchone()[0] or 0
        cursor.execute("SELECT AVG(total_amount) FROM orders")
        stats['avg_order'] = cursor.fetchone()[0] or 0

        # Средние показатели
        stats['orders_per_customer'] = stats['orders'] / max(stats['customers'], 1)
        stats['sales_per_product'] = stats['total_sales'] / max(stats['products'], 1)

        stats_text = (
            f"📈 ПОДРОБНАЯ СТАТИСТИКА СИСТЕМЫ:\n\n"
            f"👥 ПОЛЬЗОВАТЕЛИ:\n"
            f"   • Всего пользователей: {stats['users']}\n\n"
            f"📦 ТОВАРЫ:\n"
            f"   • Наименований в каталоге: {stats['products']}\n"
            f"   • Общий остаток: {stats['total_products_qty']} шт.\n\n"
            f"👤 КЛИЕНТЫ:\n"
            f"   • Всего клиентов: {stats['customers']}\n\n"
            f"📋 ЗАКАЗЫ:\n"
            f"   • Всего заказов: {stats['orders']}\n"
            f"   • Общая сумма продаж: {stats['total_sales']:.2f} ₽\n"
            f"   • Средний чек: {stats['avg_order']:.2f} ₽\n\n"
            f"🎯 ЭФФЕКТИВНОСТЬ:\n"
            f"   • Заказов на клиента: {stats['orders_per_customer']:.2f}\n"
            f"   • Продаж на товар: {stats['sales_per_product']:.2f} ₽\n\n"
            "✅ Система работает стабильно!"
        )
        stats_label = tk.Label(
            self.content_frame,
            text=stats_text,
            font=('Arial', 12),
            bg='white',
            fg='#2c3e50',
            justify='left'
        )
        stats_label.pack(pady=20)

    def exit_app(self):
        """Закрывает приложение после подтверждения."""
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти из ERP системы?"):
            if self.db.conn:
                self.db.conn.close()
            self.root.destroy()

    def run(self):
        """Запуск главного цикла приложения."""
        self.root.mainloop()


# ------------------ ФОРМЫ (ДИАЛОГИ) ------------------

class UserForm(tk.Toplevel):
    """Диалоговое окно для создания/редактирования пользователя."""

    def __init__(self, parent, title, initial=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x350")
        self.resizable(False, False)
        self.result = None

        # Поля формы
        tk.Label(self, text="Логин:", anchor='w').pack(fill='x', padx=20, pady=(20, 0))
        self.username_var = tk.StringVar(value=initial[0] if initial else "")
        tk.Entry(self, textvariable=self.username_var).pack(fill='x', padx=20)

        tk.Label(self, text="Полное имя:", anchor='w').pack(fill='x', padx=20, pady=(10, 0))
        self.fullname_var = tk.StringVar(value=initial[1] if initial else "")
        tk.Entry(self, textvariable=self.fullname_var).pack(fill='x', padx=20)

        tk.Label(self, text="Роль:", anchor='w').pack(fill='x', padx=20, pady=(10, 0))
        self.role_var = tk.StringVar(value=initial[2] if initial else "")
        tk.Entry(self, textvariable=self.role_var).pack(fill='x', padx=20)

        tk.Label(self, text="Email:", anchor='w').pack(fill='x', padx=20, pady=(10, 0))
        self.email_var = tk.StringVar(value=initial[3] if initial else "")
        tk.Entry(self, textvariable=self.email_var).pack(fill='x', padx=20)

        tk.Label(self, text="Пароль:", anchor='w').pack(fill='x', padx=20, pady=(10, 0))
        self.password_var = tk.StringVar(value=initial[4] if initial else "")
        tk.Entry(self, textvariable=self.password_var, show='*').pack(fill='x', padx=20)

        # Кнопки Сохранить/Отмена
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Сохранить", width=10, command=self.on_save, bg='#27ae60', fg='white').pack(side='left', padx=10)
        tk.Button(btn_frame, text="Отмена", width=10, command=self.destroy, bg='#e74c3c', fg='white').pack(side='left')

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def on_save(self):
        """Собирает данные и закрывает окно."""
        username = self.username_var.get().strip()
        full_name = self.fullname_var.get().strip()
        role = self.role_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        if not (username and full_name and role and password):
            messagebox.showwarning("Валидация", "Поля логин, полное имя, роль и пароль обязательны.")
            return
        self.result = (username, full_name, role, email, password)
        self.destroy()


class ProductForm(tk.Toplevel):
    """Диалоговое окно для создания/редактирования товара."""

    def __init__(self, parent, title, initial=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x300")
        self.resizable(False, False)
        self.result = None

        tk.Label(self, text="Название:", anchor='w').pack(fill='x', padx=20, pady=(20, 0))
        self.name_var = tk.StringVar(value=initial[0] if initial else "")
        tk.Entry(self, textvariable=self.name_var).pack(fill='x', padx=20)

        tk.Label(self, text="Цена (₽):", anchor='w').pack(fill='x', padx=20, pady=(10, 0))
        self.price_var = tk.DoubleVar(value=initial[1] if initial else 0.0)
        tk.Entry(self, textvariable=self.price_var).pack(fill='x', padx=20)

        tk.Label(self, text="Остаток:", anchor='w').pack(fill='x', padx=20, pady=(10, 0))
        self.qty_var = tk.IntVar(value=initial[2] if initial else 0)
        tk.Entry(self, textvariable=self.qty_var).pack(fill='x', padx=20)

        tk.Label(self, text="Категория:", anchor='w').pack(fill='x', padx=20, pady=(10, 0))
        self.category_var = tk.StringVar(value=initial[3] if initial else "")
        tk.Entry(self, textvariable=self.category_var).pack(fill='x', padx=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Сохранить", width=10, command=self.on_save, bg='#27ae60', fg='white').pack(side='left', padx=10)
        tk.Button(btn_frame, text="Отмена", width=10, command=self.destroy, bg='#e74c3c', fg='white').pack(side='left')

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def on_save(self):
        """Собирает данные о товаре и закрывает окно."""
        name = self.name_var.get().strip()
        try:
            price = float(self.price_var.get())
        except ValueError:
            messagebox.showwarning("Валидация", "Цена должна быть числом.")
            return
        try:
            quantity = int(self.qty_var.get())
        except ValueError:
            messagebox.showwarning("Валидация", "Остаток должен быть целым числом.")
            return
        category = self.category_var.get().strip()
        if not name:
            messagebox.showwarning("Валидация", "Название товара обязательно.")
            return
        self.result = (name, price, quantity, category)
        self.destroy()


class CustomerForm(tk.Toplevel):
    """Диалоговое окно для создания/редактирования клиента."""

    def __init__(self, parent, title, initial=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x300")
        self.resizable(False, False)
        self.result = None

        tk.Label(self, text="Имя/Компания:", anchor='w').pack(fill='x', padx=20, pady=(20, 0))
        self.name_var = tk.StringVar(value=initial[0] if initial else "")
        tk.Entry(self, textvariable=self.name_var).pack(fill='x', padx=20)

        tk.Label(self, text="Email:", anchor='w').pack(fill='x', padx=20, pady=(10, 0))
        self.email_var = tk.StringVar(value=initial[1] if initial else "")
        tk.Entry(self, textvariable=self.email_var).pack(fill='x', padx=20)

        tk.Label(self, text="Телефон:", anchor='w').pack(fill='x', padx=20, pady=(10, 0))
        self.phone_var = tk.StringVar(value=initial[2] if initial else "")
        tk.Entry(self, textvariable=self.phone_var).pack(fill='x', padx=20)

        tk.Label(self, text="Адрес:", anchor='w').pack(fill='x', padx=20, pady=(10, 0))
        self.address_var = tk.StringVar(value=initial[3] if initial else "")
        tk.Entry(self, textvariable=self.address_var).pack(fill='x', padx=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Сохранить", width=10, command=self.on_save, bg='#27ae60', fg='white').pack(side='left', padx=10)
        tk.Button(btn_frame, text="Отмена", width=10, command=self.destroy, bg='#e74c3c', fg='white').pack(side='left')

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def on_save(self):
        """Собирает данные о клиенте и закрывает окно."""
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_var.get().strip()
        if not name:
            messagebox.showwarning("Валидация", "Имя клиента обязательно.")
            return
        self.result = (name, email, phone, address)
        self.destroy()


class OrderForm(tk.Toplevel):
    """Диалоговое окно для создания заказа с выбором клиента и добавлением товаров."""

    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.title("Добавить заказ")
        self.geometry("600x500")
        self.resizable(False, False)
        self.db = db
        self.result = None
        self.items = []

        # Выбор клиента
        tk.Label(self, text="Выберите клиента:", anchor='w').pack(fill='x', padx=20, pady=(20, 0))
        self.customers = self.db.fetch_all('customers', order_by='name')
        cust_names = [c[1] for c in self.customers]
        self.cust_var = tk.StringVar()
        self.cust_combobox = ttk.Combobox(self, textvariable=self.cust_var, values=cust_names, state='readonly')
        self.cust_combobox.pack(fill='x', padx=20)
        if cust_names:
            self.cust_combobox.current(0)

        # Таблица для позиций заказа
        columns = ('product', 'quantity', 'price', 'subtotal')
        self.items_tree = ttk.Treeview(self, columns=columns, show='headings', height=8)
        headings = {'product': 'Товар', 'quantity': 'Кол-во', 'price': 'Цена', 'subtotal': 'Сумма'}
        for col in columns:
            self.items_tree.heading(col, text=headings[col])
            self.items_tree.column(col, width=120, anchor='center')
        self.items_tree.pack(fill='both', expand=True, padx=20, pady=(10, 0))

        # Панель добавления товара в заказ
        add_frame = tk.Frame(self)
        add_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(add_frame, text="Товар:", anchor='w').grid(row=0, column=0, padx=(0, 5), pady=5)
        self.products = self.db.fetch_all('products', order_by='name')
        prod_names = [p[1] for p in self.products]
        self.prod_var = tk.StringVar()
        self.prod_combobox = ttk.Combobox(add_frame, textvariable=self.prod_var, values=prod_names, state='readonly', width=25)
        self.prod_combobox.grid(row=0, column=1, padx=(0, 10), pady=5)
        if prod_names:
            self.prod_combobox.current(0)

        tk.Label(add_frame, text="Кол-во:", anchor='w').grid(row=0, column=2, padx=(0, 5), pady=5)
        self.item_qty_var = tk.IntVar(value=1)
        tk.Entry(add_frame, textvariable=self.item_qty_var, width=6).grid(row=0, column=3, padx=(0, 10), pady=5)

        tk.Button(add_frame, text="Добавить позицию", command=self.add_item_to_order, bg='#3498db', fg='white') \
            .grid(row=0, column=4, padx=(0, 5), pady=5)

        # Итоговая сумма заказа
        self.total_label = tk.Label(self, text="Итого: 0.00 ₽", font=('Arial', 14, 'bold'), bg='white', fg='#2c3e50', anchor='e')
        self.total_label.pack(fill='x', padx=20, pady=(5, 0))

        # Кнопки Сохранить/Отмена
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Сохранить заказ", width=15, command=self.on_save_order, bg='#27ae60', fg='white').pack(side='left', padx=10)
        tk.Button(btn_frame, text="Отмена", width=15, command=self.destroy, bg='#e74c3c', fg='white').pack(side='left')

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def add_item_to_order(self):
        """Добавляет выбранную товарную позицию в таблицу заказа."""
        prod_name = self.prod_var.get()
        qty = self.item_qty_var.get()
        if not prod_name or qty <= 0:
            messagebox.showwarning("Валидация", "Выберите товар и введите корректное количество.")
            return
        # Находим объект продукта
        prod = next((p for p in self.products if p[1] == prod_name), None)
        if not prod:
            return
        prod_id, _, price, stock_qty, _, _ = prod
        if qty > stock_qty:
            messagebox.showwarning("Недостаточно товара", f"На складе доступно только {stock_qty} шт.")
            return
        subtotal = qty * price
        # Сохраняем в списке позиций
        self.items.append({
            'product_id': prod_id,
            'product_name': prod_name,
            'quantity': qty,
            'price': price,
            'subtotal': subtotal
        })
        # Обновляем таблицу и итоговую сумму
        self.refresh_items_table()

    def refresh_items_table(self):
        """Обновляет содержимое таблицы позиций и итоговую сумму."""
        for row in self.items_tree.get_children():
            self.items_tree.delete(row)
        total = 0
        for item in self.items:
            total += item['subtotal']
            self.items_tree.insert('', 'end', values=(
                item['product_name'], item['quantity'], f"{item['price']:.2f}", f"{item['subtotal']:.2f}"
            ))
        self.total_label.config(text=f"Итого: {total:.2f} ₽")

    def on_save_order(self):
        """Сохраняет заказ и закрывает окно."""
        cust_name = self.cust_var.get()
        if not cust_name:
            messagebox.showwarning("Валидация", "Пожалуйста, выберите клиента.")
            return
        if not self.items:
            messagebox.showwarning("Валидация", "Добавьте хотя бы одну товарную позицию.")
            return
        # Находим ID клиента
        customer = next((c for c in self.customers if c[1] == cust_name), None)
        if not customer:
            return
        customer_id = customer[0]
        self.result = (customer_id, self.items)
        self.destroy()


def main():
    print("🚀 Запуск ERP системы v3.0...")
    try:
        app = SimpleERP()
        print("✅ Интерфейс создан успешно! Система готова к работе.")
        app.run()
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
