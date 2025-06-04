# -*- coding: utf-8 -*-
"""
Модуль управления заказами ERP системы
"""

import tkinter as tk
from tkinter import ttk, messagebox

class OrdersModule:
    def __init__(self, parent_frame, database):
        self.parent = parent_frame
        self.db = database
        self.create_widgets()
        self.load_orders()
        
    def create_widgets(self):
        # Заголовок модуля
        title_label = tk.Label(
            self.parent,
            text="УПРАВЛЕНИЕ ЗАКАЗАМИ",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Фрейм для кнопок управления
        buttons_frame = tk.Frame(self.parent, bg='white')
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        # Кнопки управления
        add_btn = tk.Button(
            buttons_frame,
            text="📋 Создать заказ",
            command=self.show_add_order_dialog,
            bg='#9b59b6',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            cursor='hand2'
        )
        add_btn.pack(side='left', padx=(0, 10))
        
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
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            cursor='hand2'
        )
        refresh_btn.pack(side='left')
        
        # Фрейм для таблицы
        table_frame = tk.Frame(self.parent, bg='white')
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Создаем таблицу заказов
        columns = ('ID', 'Клиент', 'Сумма', 'Статус', 'Дата создания')
        self.orders_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Настраиваем колонки
        self.orders_tree.heading('ID', text='№ Заказа')
        self.orders_tree.heading('Клиент', text='Клиент')
        self.orders_tree.heading('Сумма', text='Сумма (₽)')
        self.orders_tree.heading('Статус', text='Статус')
        self.orders_tree.heading('Дата создания', text='Дата создания')
        
        # Настраиваем ширину колонок
        self.orders_tree.column('ID', width=100)
        self.orders_tree.column('Клиент', width=200)
        self.orders_tree.column('Сумма', width=120)
        self.orders_tree.column('Статус', width=120)
        self.orders_tree.column('Дата создания', width=150)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем элементы
        self.orders_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def load_orders(self):
        """Загрузить список заказов"""
        # Очищаем таблицу
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
            
        # Загружаем заказы из базы данных
        orders = self.db.get_all_orders()
        for order in orders:
            # order = (id, customer_name, total_amount, status, created_date)
            self.orders_tree.insert('', 'end', values=(
                f"#{order[0]:04d}", order[1], f"{order[2]:.2f}", 
                order[3], order[4]
            ))
            
    def show_add_order_dialog(self):
        """Показать диалог создания заказа"""
        # Сначала получаем список клиентов
        customers = self.db.get_all_customers()
        if not customers:
            messagebox.showwarning("Внимание", "Нет клиентов в базе данных! Сначала добавьте клиентов.")
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title("Создать заказ")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        dialog.configure(bg='white')
        
        # Центрируем диалог
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        # Заголовок
        title_label = tk.Label(
            dialog,
            text="Создание нового заказа",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Фрейм для полей ввода
        fields_frame = tk.Frame(dialog, bg='white')
        fields_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Выбор клиента
        client_label = tk.Label(fields_frame, text="Клиент:", bg='white', font=('Arial', 10))
        client_label.grid(row=0, column=0, sticky='w', pady=5)
        
        # Создаем словарь клиентов для удобства
        customer_dict = {f"{c[1]} (ID: {c[0]})": c[0] for c in customers}
        customer_names = list(customer_dict.keys())
        
        client_var = tk.StringVar()
        client_combo = ttk.Combobox(
            fields_frame, 
            textvariable=client_var,
            values=customer_names,
            state="readonly",
            width=35
        )
        client_combo.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Сумма заказа
        amount_label = tk.Label(fields_frame, text="Сумма заказа (₽):", bg='white', font=('Arial', 10))
        amount_label.grid(row=1, column=0, sticky='w', pady=5)
        
        amount_var = tk.StringVar()
        amount_entry = tk.Entry(fields_frame, textvariable=amount_var, font=('Arial', 10), width=35)
        amount_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Статус заказа
        status_label = tk.Label(fields_frame, text="Статус:", bg='white', font=('Arial', 10))
        status_label.grid(row=2, column=0, sticky='w', pady=5)
        
        status_var = tk.StringVar(value="Новый")
        status_combo = ttk.Combobox(
            fields_frame, 
            textvariable=status_var,
            values=["Новый", "В обработке", "Готов к отправке", "Отправлен", "Доставлен", "Отменен"],
            state="readonly",
            width=32
        )
        status_combo.grid(row=2, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # Информационное сообщение
        info_label = tk.Label(
            dialog,
            text="💡 Это упрощенная версия создания заказа.\nВ полной версии здесь был бы выбор товаров и их количества.",
            font=('Arial', 9),
            bg='white',
            fg='#7f8c8d',
            justify='center'
        )
        info_label.pack(pady=10)
        
        # Кнопки
        buttons_frame = tk.Frame(dialog, bg='white')
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        def save_order():
            # Проверяем заполнение обязательных полей
            if not client_var.get() or not amount_var.get():
                messagebox.showerror("Ошибка", "Заполните все обязательные поля!")
                return
                
            try:
                amount = float(amount_var.get())
                if amount <= 0:
                    messagebox.showerror("Ошибка", "Сумма заказа должна быть положительной!")
                    return
                    
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат суммы заказа!")
                return
                
            # Получаем ID клиента
            customer_id = customer_dict[client_var.get()]
            
            # Добавляем заказ
            order_id = self.db.add_order(customer_id, amount, status_var.get())
            
            messagebox.showinfo("Успех", f"Заказ #{order_id:04d} успешно создан!")
            dialog.destroy()
            self.load_orders()
                
        def cancel():
            dialog.destroy()
            
        save_btn = tk.Button(
            buttons_frame,
            text="Создать заказ",
            command=save_order,
            bg='#9b59b6',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            cursor='hand2'
        )
        save_btn.pack(side='left', padx=(0, 10))
        
        cancel_btn = tk.Button(
            buttons_frame,
            text="Отмена",
            command=cancel,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            cursor='hand2'
        )
        cancel_btn.pack(side='left')
        
    def delete_selected_order(self):
        """Удалить выбранный заказ"""
        selected_item = self.orders_tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите заказ для удаления!")
            return
            
        # Получаем данные выбранного заказа
        order_data = self.orders_tree.item(selected_item[0])['values']
        order_number = order_data[0]
        order_id = int(order_number.replace('#', ''))
        
        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить заказ {order_number}?"):
            self.db.delete_order(order_id)
            messagebox.showinfo("Успех", "Заказ успешно удален!")
            self.load_orders() 