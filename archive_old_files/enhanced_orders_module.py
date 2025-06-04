# -*- coding: utf-8 -*-
"""
Улучшенный модуль управления заказами ERP системы с позициями товаров
"""

import tkinter as tk
from tkinter import ttk, messagebox

class EnhancedOrdersModule:
    def __init__(self, parent_frame, database):
        self.parent = parent_frame
        self.db = database
        self.create_widgets()
        self.load_orders()
        
    def create_widgets(self):
        # Заголовок модуля
        title_label = tk.Label(
            self.parent,
            text="УПРАВЛЕНИЕ ЗАКАЗАМИ (РАСШИРЕННАЯ ВЕРСИЯ)",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Создаем Notebook для вкладок
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Вкладка "Список заказов"
        self.orders_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.orders_frame, text="📋 Список заказов")
        
        # Вкладка "Создать заказ"
        self.create_order_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.create_order_frame, text="➕ Создать заказ")
        
        # Создаем содержимое вкладок
        self.create_orders_list_tab()
        self.create_new_order_tab()
        
    def create_orders_list_tab(self):
        """Создать вкладку со списком заказов"""
        # Фрейм для кнопок управления
        buttons_frame = tk.Frame(self.orders_frame, bg='white')
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        # Кнопки управления
        view_btn = tk.Button(
            buttons_frame,
            text="👁️ Просмотреть заказ",
            command=self.view_selected_order,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            cursor='hand2'
        )
        view_btn.pack(side='left', padx=(0, 10))
        
        delete_btn = tk.Button(
            buttons_frame,
            text="🗑️ Удалить заказ",
            command=self.delete_selected_order,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            cursor='hand2'
        )
        delete_btn.pack(side='left', padx=(0, 10))
        
        refresh_btn = tk.Button(
            buttons_frame,
            text="🔄 Обновить",
            command=self.load_orders,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            cursor='hand2'
        )
        refresh_btn.pack(side='left')
        
        # Поиск
        search_frame = tk.Frame(buttons_frame, bg='white')
        search_frame.pack(side='right')
        
        tk.Label(search_frame, text="🔍 Поиск:", bg='white', font=('Arial', 10)).pack(side='left')
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', self.filter_orders)
        
        # Фрейм для таблицы
        table_frame = tk.Frame(self.orders_frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Создаем таблицу заказов
        columns = ('ID', 'Клиент', 'Кол-во позиций', 'Сумма', 'Статус', 'Дата создания')
        self.orders_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Настраиваем колонки
        for col in columns:
            self.orders_tree.heading(col, text=col)
            
        self.orders_tree.column('ID', width=80)
        self.orders_tree.column('Клиент', width=200)
        self.orders_tree.column('Кол-во позиций', width=120)
        self.orders_tree.column('Сумма', width=120)
        self.orders_tree.column('Статус', width=120)
        self.orders_tree.column('Дата создания', width=150)
        
        # Добавляем скроллбары
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.orders_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.orders_tree.xview)
        self.orders_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Размещаем элементы
        self.orders_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
    def create_new_order_tab(self):
        """Создать вкладку для создания нового заказа"""
        # Основной фрейм с прокруткой
        canvas = tk.Canvas(self.create_order_frame, bg='white')
        scrollbar = ttk.Scrollbar(self.create_order_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Информация о заказе
        order_info_frame = tk.LabelFrame(scrollable_frame, text="Информация о заказе", bg='white', font=('Arial', 12, 'bold'))
        order_info_frame.pack(fill='x', padx=20, pady=10)
        
        # Выбор клиента
        client_frame = tk.Frame(order_info_frame, bg='white')
        client_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(client_frame, text="Клиент:", bg='white', font=('Arial', 10, 'bold')).pack(side='left')
        
        self.client_var = tk.StringVar()
        self.client_combo = ttk.Combobox(client_frame, textvariable=self.client_var, state="readonly", width=40)
        self.client_combo.pack(side='left', padx=10)
        
        # Статус заказа
        status_frame = tk.Frame(order_info_frame, bg='white')
        status_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(status_frame, text="Статус:", bg='white', font=('Arial', 10, 'bold')).pack(side='left')
        
        self.status_var = tk.StringVar(value="Новый")
        status_combo = ttk.Combobox(
            status_frame,
            textvariable=self.status_var,
            values=["Новый", "В обработке", "Готов к отправке", "Отправлен", "Доставлен", "Отменен"],
            state="readonly",
            width=20
        )
        status_combo.pack(side='left', padx=10)
        
        # Позиции заказа
        items_frame = tk.LabelFrame(scrollable_frame, text="Позиции заказа", bg='white', font=('Arial', 12, 'bold'))
        items_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Добавление позиции
        add_item_frame = tk.Frame(items_frame, bg='white')
        add_item_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(add_item_frame, text="Товар:", bg='white', font=('Arial', 10)).pack(side='left')
        
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(add_item_frame, textvariable=self.product_var, state="readonly", width=30)
        self.product_combo.pack(side='left', padx=5)
        
        tk.Label(add_item_frame, text="Кол-во:", bg='white', font=('Arial', 10)).pack(side='left', padx=(10, 0))
        
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = tk.Entry(add_item_frame, textvariable=self.quantity_var, width=10)
        quantity_entry.pack(side='left', padx=5)
        
        add_btn = tk.Button(
            add_item_frame,
            text="➕ Добавить",
            command=self.add_order_item,
            bg='#27ae60',
            fg='white',
            font=('Arial', 9, 'bold'),
            relief='flat'
        )
        add_btn.pack(side='left', padx=10)
        
        # Таблица позиций заказа
        items_table_frame = tk.Frame(items_frame, bg='white')
        items_table_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('Товар', 'Цена', 'Количество', 'Сумма')
        self.items_tree = ttk.Treeview(items_table_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=150)
        
        items_scrollbar = ttk.Scrollbar(items_table_frame, orient='vertical', command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=items_scrollbar.set)
        
        self.items_tree.pack(side='left', fill='both', expand=True)
        items_scrollbar.pack(side='right', fill='y')
        
        # Кнопка удаления позиции
        remove_item_btn = tk.Button(
            items_frame,
            text="🗑️ Удалить позицию",
            command=self.remove_order_item,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 9, 'bold'),
            relief='flat'
        )
        remove_item_btn.pack(pady=5)
        
        # Итоговая информация
        total_frame = tk.Frame(scrollable_frame, bg='#ecf0f1', relief='raised', bd=2)
        total_frame.pack(fill='x', padx=20, pady=10)
        
        self.total_label = tk.Label(
            total_frame,
            text="Общая сумма заказа: 0.00 ₽",
            font=('Arial', 14, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.total_label.pack(pady=10)
        
        # Кнопки управления заказом
        buttons_frame = tk.Frame(scrollable_frame, bg='white')
        buttons_frame.pack(fill='x', padx=20, pady=20)
        
        create_btn = tk.Button(
            buttons_frame,
            text="💾 Создать заказ",
            command=self.create_order,
            bg='#9b59b6',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='flat',
            cursor='hand2',
            pady=10
        )
        create_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = tk.Button(
            buttons_frame,
            text="🗑️ Очистить форму",
            command=self.clear_order_form,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='flat',
            cursor='hand2',
            pady=10
        )
        clear_btn.pack(side='left')
        
        # Размещаем canvas и scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Загружаем данные для комбобоксов
        self.load_form_data()
        
        # Инициализируем список позиций заказа
        self.order_items = []
        
    def load_form_data(self):
        """Загрузить данные для комбобоксов"""
        # Загружаем клиентов
        customers = self.db.get_all_customers()
        customer_list = [f"{c[1]} (ID: {c[0]})" for c in customers]
        self.client_combo['values'] = customer_list
        
        # Загружаем товары
        products = self.db.get_all_products()
        product_list = [f"{p[1]} - {p[3]:.2f} ₽ (остаток: {p[4]}) (ID: {p[0]})" for p in products if p[4] > 0]
        self.product_combo['values'] = product_list
        
    def add_order_item(self):
        """Добавить позицию в заказ"""
        if not self.product_var.get() or not self.quantity_var.get():
            messagebox.showwarning("Внимание", "Выберите товар и укажите количество!")
            return
            
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть положительным числом!")
            return
            
        # Извлекаем ID товара из строки
        product_text = self.product_var.get()
        product_id = int(product_text.split("(ID: ")[1].split(")")[0])
        
        # Получаем информацию о товаре из базы данных
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, quantity FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        conn.close()
        
        if not product:
            messagebox.showerror("Ошибка", "Товар не найден!")
            return
            
        if product[2] < quantity:
            messagebox.showerror("Ошибка", f"Недостаточно товара на складе! Доступно: {product[2]}")
            return
            
        # Проверяем, нет ли уже такого товара в заказе
        for item in self.order_items:
            if item['product_id'] == product_id:
                messagebox.showwarning("Внимание", "Этот товар уже добавлен в заказ!")
                return
                
        # Добавляем позицию
        item = {
            'product_id': product_id,
            'name': product[0],
            'price': product[1],
            'quantity': quantity,
            'total': product[1] * quantity
        }
        
        self.order_items.append(item)
        
        # Обновляем таблицу позиций
        self.update_items_table()
        
        # Очищаем поля
        self.product_var.set("")
        self.quantity_var.set("1")
        
    def remove_order_item(self):
        """Удалить позицию из заказа"""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите позицию для удаления!")
            return
            
        # Получаем индекс выбранной позиции
        item_index = self.items_tree.index(selected[0])
        
        # Удаляем позицию
        del self.order_items[item_index]
        
        # Обновляем таблицу
        self.update_items_table()
        
    def update_items_table(self):
        """Обновить таблицу позиций заказа"""
        # Очищаем таблицу
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
            
        # Добавляем позиции
        total_sum = 0
        for item in self.order_items:
            self.items_tree.insert('', 'end', values=(
                item['name'],
                f"{item['price']:.2f} ₽",
                item['quantity'],
                f"{item['total']:.2f} ₽"
            ))
            total_sum += item['total']
            
        # Обновляем общую сумму
        self.total_label.config(text=f"Общая сумма заказа: {total_sum:.2f} ₽")
        
    def create_order(self):
        """Создать заказ"""
        if not self.client_var.get():
            messagebox.showerror("Ошибка", "Выберите клиента!")
            return
            
        if not self.order_items:
            messagebox.showerror("Ошибка", "Добавьте хотя бы одну позицию в заказ!")
            return
            
        try:
            # Извлекаем ID клиента
            client_text = self.client_var.get()
            client_id = int(client_text.split("(ID: ")[1].split(")")[0])
            
            # Вычисляем общую сумму
            total_amount = sum(item['total'] for item in self.order_items)
            
            # Создаем заказ
            order_id = self.db.add_order(client_id, total_amount, self.status_var.get())
            
            # Добавляем позиции заказа
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            for item in self.order_items:
                cursor.execute('''
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (?, ?, ?, ?)
                ''', (order_id, item['product_id'], item['quantity'], item['price']))
                
                # Обновляем количество товара на складе
                cursor.execute('''
                    UPDATE products 
                    SET quantity = quantity - ? 
                    WHERE id = ?
                ''', (item['quantity'], item['product_id']))
                
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Успех", f"Заказ #{order_id:04d} успешно создан!")
            
            # Очищаем форму
            self.clear_order_form()
            
            # Обновляем список заказов
            self.load_orders()
            
            # Переключаемся на вкладку со списком заказов
            self.notebook.select(0)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать заказ: {e}")
            
    def clear_order_form(self):
        """Очистить форму создания заказа"""
        self.client_var.set("")
        self.status_var.set("Новый")
        self.product_var.set("")
        self.quantity_var.set("1")
        self.order_items = []
        self.update_items_table()
        
    def load_orders(self):
        """Загрузить список заказов"""
        # Очищаем таблицу
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
            
        # Загружаем заказы из базы данных
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.id, c.name, 
                   COUNT(oi.id) as items_count,
                   o.total_amount, o.status, o.created_date 
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            LEFT JOIN order_items oi ON o.id = oi.order_id
            GROUP BY o.id, c.name, o.total_amount, o.status, o.created_date
            ORDER BY o.created_date DESC
        ''')
        orders = cursor.fetchall()
        conn.close()
        
        for order in orders:
            self.orders_tree.insert('', 'end', values=(
                f"#{order[0]:04d}",
                order[1],
                order[2] if order[2] else 0,
                f"{order[3]:.2f} ₽",
                order[4],
                order[5]
            ))
            
    def filter_orders(self, event=None):
        """Фильтрация заказов по поисковому запросу"""
        query = self.search_var.get().lower()
        
        # Очищаем таблицу
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
            
        # Загружаем все заказы
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.id, c.name, 
                   COUNT(oi.id) as items_count,
                   o.total_amount, o.status, o.created_date 
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            LEFT JOIN order_items oi ON o.id = oi.order_id
            GROUP BY o.id, c.name, o.total_amount, o.status, o.created_date
            ORDER BY o.created_date DESC
        ''')
        orders = cursor.fetchall()
        conn.close()
        
        # Фильтруем и отображаем
        for order in orders:
            if (query in order[1].lower() or 
                query in order[4].lower() or 
                query in f"#{order[0]:04d}".lower()):
                self.orders_tree.insert('', 'end', values=(
                    f"#{order[0]:04d}",
                    order[1],
                    order[2] if order[2] else 0,
                    f"{order[3]:.2f} ₽",
                    order[4],
                    order[5]
                ))
                
    def view_selected_order(self):
        """Просмотр выбранного заказа"""
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите заказ для просмотра!")
            return
            
        # Получаем ID заказа
        order_data = self.orders_tree.item(selected[0])['values']
        order_id = int(order_data[0].replace('#', ''))
        
        # Создаем окно просмотра заказа
        self.show_order_details(order_id)
        
    def show_order_details(self, order_id):
        """Показать детали заказа"""
        details_window = tk.Toplevel(self.parent)
        details_window.title(f"Заказ #{order_id:04d}")
        details_window.geometry("700x500")
        details_window.configure(bg='white')
        
        # Получаем информацию о заказе
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Основная информация о заказе
        cursor.execute('''
            SELECT o.*, c.name as customer_name, c.email, c.phone, c.address
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            WHERE o.id = ?
        ''', (order_id,))
        order = cursor.fetchone()
        
        # Позиции заказа
        cursor.execute('''
            SELECT oi.*, p.name as product_name
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        items = cursor.fetchall()
        
        conn.close()
        
        if not order:
            messagebox.showerror("Ошибка", "Заказ не найден!")
            return
            
        # Заголовок
        title_label = tk.Label(
            details_window,
            text=f"ЗАКАЗ #{order_id:04d}",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Информация о заказе и клиенте
        info_frame = tk.Frame(details_window, bg='#ecf0f1', relief='raised', bd=2)
        info_frame.pack(fill='x', padx=20, pady=10)
        
        info_text = f"""
Клиент: {order[7]}
Email: {order[8] or 'Не указан'}
Телефон: {order[9] or 'Не указан'}
Адрес: {order[10] or 'Не указан'}

Статус заказа: {order[3]}
Дата создания: {order[4]}
Общая сумма: {order[2]:.2f} ₽
        """
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 10),
            bg='#ecf0f1',
            fg='#2c3e50',
            justify='left'
        )
        info_label.pack(padx=20, pady=15)
        
        # Позиции заказа
        items_label = tk.Label(
            details_window,
            text="Позиции заказа:",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        items_label.pack(anchor='w', padx=20, pady=(10, 5))
        
        # Таблица позиций
        items_frame = tk.Frame(details_window, bg='white')
        items_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        columns = ('Товар', 'Цена за ед.', 'Количество', 'Сумма')
        items_tree = ttk.Treeview(items_frame, columns=columns, show='headings')
        
        for col in columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, width=150)
            
        for item in items:
            items_tree.insert('', 'end', values=(
                item[5],  # product_name
                f"{item[4]:.2f} ₽",  # price
                item[3],  # quantity
                f"{item[3] * item[4]:.2f} ₽"  # total
            ))
            
        items_tree.pack(fill='both', expand=True)
        
    def delete_selected_order(self):
        """Удалить выбранный заказ"""
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите заказ для удаления!")
            return
            
        # Получаем данные выбранного заказа
        order_data = self.orders_tree.item(selected[0])['values']
        order_number = order_data[0]
        order_id = int(order_number.replace('#', ''))
        
        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить заказ {order_number}?"):
            # Возвращаем товары на склад перед удалением заказа
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Получаем позиции заказа
            cursor.execute('''
                SELECT product_id, quantity 
                FROM order_items 
                WHERE order_id = ?
            ''', (order_id,))
            items = cursor.fetchall()
            
            # Возвращаем товары на склад
            for item in items:
                cursor.execute('''
                    UPDATE products 
                    SET quantity = quantity + ? 
                    WHERE id = ?
                ''', (item[1], item[0]))
                
            conn.commit()
            conn.close()
            
            # Удаляем заказ (позиции удалятся автоматически через foreign key)
            self.db.delete_order(order_id)
            messagebox.showinfo("Успех", "Заказ успешно удален, товары возвращены на склад!")
            self.load_orders() 