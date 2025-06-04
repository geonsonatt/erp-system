# -*- coding: utf-8 -*-
"""
Модуль для работы с базой данных ERP системы
"""

import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_name="erp_database.db"):
        self.db_name = db_name
        self.init_database()
        
    def get_connection(self):
        """Получить соединение с базой данных"""
        return sqlite3.connect(self.db_name)
        
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Таблица пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    email TEXT,
                    created_date TEXT NOT NULL
                )
            ''')
            
            # Таблица товаров
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    category TEXT,
                    created_date TEXT NOT NULL
                )
            ''')
            
            # Таблица клиентов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    created_date TEXT NOT NULL
                )
            ''')
            
            # Таблица заказов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    total_amount REAL NOT NULL,
                    status TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                )
            ''')
            
            # Таблица позиций заказов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')
            
            conn.commit()
            
            # Добавляем тестовые данные при первом запуске
            self.insert_sample_data(cursor)
            
        except Exception as e:
            print(f"Ошибка при инициализации базы данных: {e}")
        finally:
            conn.close()
            
    def insert_sample_data(self, cursor):
        """Добавление тестовых данных"""
        # Проверяем, есть ли уже данные
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 0:
            return
            
        # Добавляем тестовых пользователей
        users_data = [
            ('admin', 'admin123', 'Администратор Системы', 'Администратор', 'admin@company.com'),
            ('manager', 'manager123', 'Иван Менеджеров', 'Менеджер', 'manager@company.com'),
            ('operator', 'operator123', 'Петр Операторов', 'Оператор', 'operator@company.com')
        ]
        
        for user in users_data:
            cursor.execute('''
                INSERT INTO users (username, password, full_name, role, email, created_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (*user, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
        # Добавляем тестовые товары
        products_data = [
            ('Компьютер ASUS', 'Настольный компьютер для офиса', 45000.0, 10, 'Электроника'),
            ('Клавиатура Logitech', 'Беспроводная клавиатура', 3500.0, 25, 'Аксессуары'),
            ('Монитор Samsung 24"', 'ЖК монитор 24 дюйма', 15000.0, 8, 'Электроника'),
            ('Мышь Logitech', 'Оптическая мышь', 1200.0, 30, 'Аксессуары'),
            ('Принтер HP LaserJet', 'Лазерный принтер', 8500.0, 5, 'Оргтехника')
        ]
        
        for product in products_data:
            cursor.execute('''
                INSERT INTO products (name, description, price, quantity, category, created_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (*product, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
        # Добавляем тестовых клиентов
        customers_data = [
            ('ООО "Рога и Копыта"', 'info@rogaikopyta.ru', '+7-495-123-45-67', 'Москва, ул. Ленина, 1'),
            ('ИП Петров И.И.', 'petrov@mail.ru', '+7-812-987-65-43', 'СПб, пр. Невский, 100'),
            ('ООО "Светлое Будущее"', 'future@mail.ru', '+7-495-555-44-33', 'Москва, ул. Мира, 50')
        ]
        
        for customer in customers_data:
            cursor.execute('''
                INSERT INTO customers (name, email, phone, address, created_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (*customer, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
        print("Тестовые данные добавлены в базу данных")
        
    # Методы для работы с пользователями
    def get_all_users(self):
        """Получить всех пользователей"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY created_date DESC")
        users = cursor.fetchall()
        conn.close()
        return users
        
    def add_user(self, username, password, full_name, role, email=""):
        """Добавить нового пользователя"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password, full_name, role, email, created_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, password, full_name, role, email, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
            
    def delete_user(self, user_id):
        """Удалить пользователя"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        
    # Методы для работы с товарами
    def get_all_products(self):
        """Получить все товары"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products ORDER BY created_date DESC")
        products = cursor.fetchall()
        conn.close()
        return products
        
    def add_product(self, name, description, price, quantity, category):
        """Добавить новый товар"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (name, description, price, quantity, category, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, description, price, quantity, category, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
        
    def delete_product(self, product_id):
        """Удалить товар"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()
        
    # Методы для работы с клиентами
    def get_all_customers(self):
        """Получить всех клиентов"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers ORDER BY created_date DESC")
        customers = cursor.fetchall()
        conn.close()
        return customers
        
    def add_customer(self, name, email, phone, address):
        """Добавить нового клиента"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customers (name, email, phone, address, created_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, phone, address, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
        
    def delete_customer(self, customer_id):
        """Удалить клиента"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()
        conn.close()
        
    # Методы для работы с заказами
    def get_all_orders(self):
        """Получить все заказы с информацией о клиентах"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.id, c.name, o.total_amount, o.status, o.created_date 
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            ORDER BY o.created_date DESC
        ''')
        orders = cursor.fetchall()
        conn.close()
        return orders
        
    def add_order(self, customer_id, total_amount, status="Новый"):
        """Добавить новый заказ"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (customer_id, total_amount, status, created_date)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, total_amount, status, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return order_id
        
    def delete_order(self, order_id):
        """Удалить заказ"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        conn.close()
        
    # Методы для отчетов
    def get_total_sales(self):
        """Получить общую сумму продаж"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(total_amount) FROM orders")
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0
        
    def get_total_products(self):
        """Получить общее количество товаров"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        result = cursor.fetchone()[0]
        conn.close()
        return result
        
    def get_total_customers(self):
        """Получить общее количество клиентов"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers")
        result = cursor.fetchone()[0]
        conn.close()
        return result
        
    def get_total_orders(self):
        """Получить общее количество заказов"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM orders")
        result = cursor.fetchone()[0]
        conn.close()
        return result 