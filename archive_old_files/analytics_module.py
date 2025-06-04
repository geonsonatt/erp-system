# -*- coding: utf-8 -*-
"""
Модуль графической аналитики ERP системы
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import Canvas
import math

class AnalyticsModule:
    def __init__(self, parent_frame, database):
        self.parent = parent_frame
        self.db = database
        self.create_widgets()
        self.load_analytics()
        
    def create_widgets(self):
        # Заголовок модуля
        title_label = tk.Label(
            self.parent,
            text="📊 ГРАФИЧЕСКАЯ АНАЛИТИКА",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Создаем Notebook для разных видов аналитики
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Вкладка "Продажи"
        self.sales_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.sales_frame, text="💰 Анализ продаж")
        
        # Вкладка "Товары"
        self.products_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.products_frame, text="📦 Анализ товаров")
        
        # Вкладка "Клиенты"
        self.customers_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.customers_frame, text="👥 Анализ клиентов")
        
        # Создаем содержимое вкладок
        self.create_sales_analytics()
        self.create_products_analytics()
        self.create_customers_analytics()
        
    def create_sales_analytics(self):
        """Создать аналитику продаж"""
        # Кнопка обновления
        refresh_btn = tk.Button(
            self.sales_frame,
            text="🔄 Обновить данные",
            command=self.update_sales_chart,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        refresh_btn.pack(pady=10)
        
        # Фрейм для статистики
        stats_frame = tk.Frame(self.sales_frame, bg='#ecf0f1', relief='raised', bd=2)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        self.sales_stats_label = tk.Label(
            stats_frame,
            text="Загрузка статистики...",
            font=('Arial', 12),
            bg='#ecf0f1',
            fg='#2c3e50',
            justify='left'
        )
        self.sales_stats_label.pack(padx=20, pady=15)
        
        # Canvas для диаграммы
        self.sales_canvas = Canvas(
            self.sales_frame,
            width=600,
            height=400,
            bg='white',
            relief='sunken',
            bd=2
        )
        self.sales_canvas.pack(pady=20)
        
    def create_products_analytics(self):
        """Создать аналитику товаров"""
        # Кнопка обновления
        refresh_btn = tk.Button(
            self.products_frame,
            text="🔄 Обновить данные",
            command=self.update_products_chart,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        refresh_btn.pack(pady=10)
        
        # Информация о товарах
        info_frame = tk.Frame(self.products_frame, bg='#ecf0f1', relief='raised', bd=2)
        info_frame.pack(fill='x', padx=20, pady=10)
        
        self.products_info_label = tk.Label(
            info_frame,
            text="Загрузка информации о товарах...",
            font=('Arial', 12),
            bg='#ecf0f1',
            fg='#2c3e50',
            justify='left'
        )
        self.products_info_label.pack(padx=20, pady=15)
        
        # Canvas для круговой диаграммы категорий
        self.products_canvas = Canvas(
            self.products_frame,
            width=600,
            height=400,
            bg='white',
            relief='sunken',
            bd=2
        )
        self.products_canvas.pack(pady=20)
        
    def create_customers_analytics(self):
        """Создать аналитику клиентов"""
        # Кнопка обновления
        refresh_btn = tk.Button(
            self.customers_frame,
            text="🔄 Обновить данные",
            command=self.update_customers_chart,
            bg='#e67e22',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        refresh_btn.pack(pady=10)
        
        # Информация о клиентах
        info_frame = tk.Frame(self.customers_frame, bg='#ecf0f1', relief='raised', bd=2)
        info_frame.pack(fill='x', padx=20, pady=10)
        
        self.customers_info_label = tk.Label(
            info_frame,
            text="Загрузка информации о клиентах...",
            font=('Arial', 12),
            bg='#ecf0f1',
            fg='#2c3e50',
            justify='left'
        )
        self.customers_info_label.pack(padx=20, pady=15)
        
        # Canvas для диаграммы активности клиентов
        self.customers_canvas = Canvas(
            self.customers_frame,
            width=600,
            height=400,
            bg='white',
            relief='sunken',
            bd=2
        )
        self.customers_canvas.pack(pady=20)
        
    def load_analytics(self):
        """Загрузить все аналитические данные"""
        self.update_sales_chart()
        self.update_products_chart()
        self.update_customers_chart()
        
    def update_sales_chart(self):
        """Обновить диаграмму продаж"""
        # Получаем данные о заказах по статусам
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT status, COUNT(*) as count, SUM(total_amount) as total
            FROM orders 
            GROUP BY status
        ''')
        sales_data = cursor.fetchall()
        
        cursor.execute('SELECT SUM(total_amount) FROM orders')
        total_sales = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT COUNT(*) FROM orders')
        total_orders = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT AVG(total_amount) FROM orders')
        avg_order = cursor.fetchone()[0] or 0
        
        conn.close()
        
        # Обновляем статистику
        stats_text = f"""
📊 СТАТИСТИКА ПРОДАЖ:

💰 Общая сумма продаж: {total_sales:.2f} ₽
📋 Всего заказов: {total_orders}
📈 Средний чек: {avg_order:.2f} ₽

ЗАКАЗЫ ПО СТАТУСАМ:
"""
        for status, count, total in sales_data:
            percentage = (count / total_orders * 100) if total_orders > 0 else 0
            stats_text += f"• {status}: {count} заказов ({percentage:.1f}%) - {total:.2f} ₽\n"
            
        self.sales_stats_label.config(text=stats_text)
        
        # Рисуем столбчатую диаграмму
        self.draw_bar_chart(self.sales_canvas, sales_data, "Заказы по статусам")
        
    def update_products_chart(self):
        """Обновить диаграмму товаров"""
        # Получаем данные о товарах по категориям
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, COUNT(*) as count, SUM(quantity * price) as value
            FROM products 
            GROUP BY category
        ''')
        categories_data = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM products')
        total_products = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT SUM(quantity * price) FROM products')
        total_value = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT SUM(quantity) FROM products')
        total_quantity = cursor.fetchone()[0] or 0
        
        conn.close()
        
        # Обновляем информацию
        info_text = f"""
📦 АНАЛИЗ ТОВАРОВ:

🏷️ Всего товаров: {total_products}
📊 Общая стоимость склада: {total_value:.2f} ₽
📈 Общее количество: {total_quantity} шт.

ТОВАРЫ ПО КАТЕГОРИЯМ:
"""
        for category, count, value in categories_data:
            percentage = (count / total_products * 100) if total_products > 0 else 0
            info_text += f"• {category}: {count} товаров ({percentage:.1f}%) - {value:.2f} ₽\n"
            
        self.products_info_label.config(text=info_text)
        
        # Рисуем круговую диаграмму
        self.draw_pie_chart(self.products_canvas, categories_data, "Распределение товаров по категориям")
        
    def update_customers_chart(self):
        """Обновить диаграмму клиентов"""
        # Получаем данные о заказах клиентов
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.name, COUNT(o.id) as orders_count, 
                   COALESCE(SUM(o.total_amount), 0) as total_spent
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            GROUP BY c.id, c.name
            ORDER BY total_spent DESC
            LIMIT 10
        ''')
        customers_data = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM customers')
        total_customers = cursor.fetchone()[0] or 0
        
        cursor.execute('''
            SELECT COUNT(DISTINCT customer_id) 
            FROM orders
        ''')
        active_customers = cursor.fetchone()[0] or 0
        
        conn.close()
        
        # Обновляем информацию
        info_text = f"""
👥 АНАЛИЗ КЛИЕНТОВ:

🏢 Всего клиентов: {total_customers}
✅ Активных клиентов: {active_customers}
📊 Конверсия: {(active_customers/total_customers*100 if total_customers > 0 else 0):.1f}%

ТОП-10 КЛИЕНТОВ ПО СУММЕ ЗАКАЗОВ:
"""
        for i, (name, orders, total) in enumerate(customers_data[:5], 1):
            info_text += f"{i}. {name}: {orders} заказов - {total:.2f} ₽\n"
            
        self.customers_info_label.config(text=info_text)
        
        # Рисуем горизонтальную диаграмму
        self.draw_horizontal_bar_chart(self.customers_canvas, customers_data, "Топ клиентов по сумме заказов")
        
    def draw_bar_chart(self, canvas, data, title):
        """Нарисовать столбчатую диаграмму"""
        canvas.delete("all")
        
        if not data:
            canvas.create_text(300, 200, text="Нет данных для отображения", 
                             font=('Arial', 14), fill='#7f8c8d')
            return
            
        # Параметры диаграммы
        width = 600
        height = 400
        margin = 60
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        # Заголовок
        canvas.create_text(width//2, 20, text=title, font=('Arial', 14, 'bold'), fill='#2c3e50')
        
        # Находим максимальное значение
        max_value = max(item[1] for item in data)  # количество заказов
        
        # Рисуем столбцы
        bar_width = chart_width // len(data) - 10
        colors = ['#3498db', '#e74c3c', '#27ae60', '#f39c12', '#9b59b6', '#34495e']
        
        for i, (status, count, total) in enumerate(data):
            x = margin + i * (chart_width // len(data)) + 5
            bar_height = (count / max_value) * chart_height if max_value > 0 else 0
            y = height - margin - bar_height
            
            # Столбец
            color = colors[i % len(colors)]
            canvas.create_rectangle(x, y, x + bar_width, height - margin, 
                                  fill=color, outline='#2c3e50', width=2)
            
            # Значение на столбце
            canvas.create_text(x + bar_width//2, y - 10, text=str(count), 
                             font=('Arial', 10, 'bold'), fill='#2c3e50')
            
            # Подпись статуса
            canvas.create_text(x + bar_width//2, height - margin + 20, 
                             text=status[:8] + '...' if len(status) > 8 else status, 
                             font=('Arial', 9), fill='#2c3e50', angle=0)
                             
        # Оси
        canvas.create_line(margin, height - margin, width - margin, height - margin, 
                         width=2, fill='#2c3e50')  # X
        canvas.create_line(margin, margin, margin, height - margin, 
                         width=2, fill='#2c3e50')  # Y
                         
    def draw_pie_chart(self, canvas, data, title):
        """Нарисовать круговую диаграмму"""
        canvas.delete("all")
        
        if not data:
            canvas.create_text(300, 200, text="Нет данных для отображения", 
                             font=('Arial', 14), fill='#7f8c8d')
            return
            
        # Заголовок
        canvas.create_text(300, 20, text=title, font=('Arial', 14, 'bold'), fill='#2c3e50')
        
        # Параметры круга
        center_x, center_y = 250, 200
        radius = 100
        
        # Общее количество
        total = sum(item[1] for item in data)
        
        # Цвета
        colors = ['#3498db', '#e74c3c', '#27ae60', '#f39c12', '#9b59b6', '#34495e', '#1abc9c', '#e67e22']
        
        # Рисуем сектора
        start_angle = 0
        legend_y = 80
        
        for i, (category, count, value) in enumerate(data):
            if total == 0:
                continue
                
            # Угол сектора
            angle = (count / total) * 360
            end_angle = start_angle + angle
            
            # Цвет
            color = colors[i % len(colors)]
            
            # Рисуем сектор
            if angle > 0:
                self.draw_pie_slice(canvas, center_x, center_y, radius, start_angle, end_angle, color)
                
            # Легенда
            legend_x = 450
            canvas.create_rectangle(legend_x, legend_y + i * 25, legend_x + 15, legend_y + i * 25 + 15, 
                                  fill=color, outline='#2c3e50')
            canvas.create_text(legend_x + 20, legend_y + i * 25 + 7, 
                             text=f"{category}: {count} ({count/total*100:.1f}%)", 
                             font=('Arial', 9), fill='#2c3e50', anchor='w')
            
            start_angle = end_angle
            
    def draw_pie_slice(self, canvas, x, y, radius, start_angle, end_angle, color):
        """Нарисовать сектор круговой диаграммы"""
        # Конвертируем углы в радианы
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Точки для дуги
        x1 = x + radius * math.cos(start_rad)
        y1 = y + radius * math.sin(start_rad)
        x2 = x + radius * math.cos(end_rad)
        y2 = y + radius * math.sin(end_rad)
        
        # Создаем полигон
        points = [x, y, x1, y1]
        
        # Добавляем точки дуги
        num_points = max(2, int(abs(end_angle - start_angle) / 5))
        for i in range(num_points + 1):
            angle = start_rad + (end_rad - start_rad) * i / num_points
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            points.extend([px, py])
            
        points.extend([x2, y2])
        
        # Рисуем полигон
        canvas.create_polygon(points, fill=color, outline='#2c3e50', width=2)
        
    def draw_horizontal_bar_chart(self, canvas, data, title):
        """Нарисовать горизонтальную столбчатую диаграмму"""
        canvas.delete("all")
        
        if not data:
            canvas.create_text(300, 200, text="Нет данных для отображения", 
                             font=('Arial', 14), fill='#7f8c8d')
            return
            
        # Заголовок
        canvas.create_text(300, 20, text=title, font=('Arial', 14, 'bold'), fill='#2c3e50')
        
        # Показываем только топ-5
        display_data = data[:5]
        
        # Параметры диаграммы
        margin = 80
        chart_height = 300
        chart_width = 400
        
        if not display_data:
            return
            
        # Максимальное значение
        max_value = max(item[2] for item in display_data)  # total_spent
        
        # Рисуем полосы
        bar_height = chart_height // len(display_data) - 10
        colors = ['#3498db', '#e74c3c', '#27ae60', '#f39c12', '#9b59b6']
        
        for i, (name, orders, total) in enumerate(display_data):
            y = 60 + i * (chart_height // len(display_data))
            bar_width = (total / max_value) * chart_width if max_value > 0 else 0
            
            # Полоса
            color = colors[i % len(colors)]
            canvas.create_rectangle(margin, y, margin + bar_width, y + bar_height, 
                                  fill=color, outline='#2c3e50', width=2)
            
            # Имя клиента
            display_name = name[:15] + '...' if len(name) > 15 else name
            canvas.create_text(margin - 5, y + bar_height//2, text=display_name, 
                             font=('Arial', 9), fill='#2c3e50', anchor='e')
            
            # Значение
            canvas.create_text(margin + bar_width + 5, y + bar_height//2, 
                             text=f"{total:.0f} ₽", 
                             font=('Arial', 9, 'bold'), fill='#2c3e50', anchor='w') 