# -*- coding: utf-8 -*-
"""
Модуль управления клиентами ERP системы
"""

import tkinter as tk
from tkinter import ttk, messagebox

class CustomersModule:
    def __init__(self, parent_frame, database):
        self.parent = parent_frame
        self.db = database
        self.create_widgets()
        self.load_customers()
        
    def create_widgets(self):
        # Заголовок модуля
        title_label = tk.Label(
            self.parent,
            text="УПРАВЛЕНИЕ КЛИЕНТАМИ",
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
            text="👤 Добавить клиента",
            command=self.show_add_customer_dialog,
            bg='#e67e22',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            cursor='hand2'
        )
        add_btn.pack(side='left', padx=(0, 10))
        
        delete_btn = tk.Button(
            buttons_frame,
            text="🗑️ Удалить клиента",
            command=self.delete_selected_customer,
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
            command=self.load_customers,
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
        
        # Создаем таблицу клиентов
        columns = ('ID', 'Название', 'Email', 'Телефон', 'Адрес', 'Дата создания')
        self.customers_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Настраиваем колонки
        self.customers_tree.heading('ID', text='ID')
        self.customers_tree.heading('Название', text='Название')
        self.customers_tree.heading('Email', text='Email')
        self.customers_tree.heading('Телефон', text='Телефон')
        self.customers_tree.heading('Адрес', text='Адрес')
        self.customers_tree.heading('Дата создания', text='Дата создания')
        
        # Настраиваем ширину колонок
        self.customers_tree.column('ID', width=50)
        self.customers_tree.column('Название', width=200)
        self.customers_tree.column('Email', width=150)
        self.customers_tree.column('Телефон', width=120)
        self.customers_tree.column('Адрес', width=200)
        self.customers_tree.column('Дата создания', width=120)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.customers_tree.yview)
        self.customers_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем элементы
        self.customers_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def load_customers(self):
        """Загрузить список клиентов"""
        # Очищаем таблицу
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
            
        # Загружаем клиентов из базы данных
        customers = self.db.get_all_customers()
        for customer in customers:
            # customer = (id, name, email, phone, address, created_date)
            self.customers_tree.insert('', 'end', values=(
                customer[0], customer[1], customer[2], customer[3], 
                customer[4], customer[5]
            ))
            
    def show_add_customer_dialog(self):
        """Показать диалог добавления клиента"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Добавить клиента")
        dialog.geometry("450x300")
        dialog.resizable(False, False)
        dialog.configure(bg='white')
        
        # Центрируем диалог
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        # Заголовок
        title_label = tk.Label(
            dialog,
            text="Добавление нового клиента",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Фрейм для полей ввода
        fields_frame = tk.Frame(dialog, bg='white')
        fields_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Поля ввода
        fields = [
            ("Название:", tk.StringVar()),
            ("Email:", tk.StringVar()),
            ("Телефон:", tk.StringVar())
        ]
        
        entries = {}
        for i, (label_text, var) in enumerate(fields):
            label = tk.Label(fields_frame, text=label_text, bg='white', font=('Arial', 10))
            label.grid(row=i, column=0, sticky='w', pady=5)
            
            entry = tk.Entry(fields_frame, textvariable=var, font=('Arial', 10), width=25)
            entry.grid(row=i, column=1, sticky='ew', pady=5, padx=(10, 0))
            entries[label_text] = var
            
        # Адрес
        addr_label = tk.Label(fields_frame, text="Адрес:", bg='white', font=('Arial', 10))
        addr_label.grid(row=len(fields), column=0, sticky='nw', pady=5)
        
        addr_text = tk.Text(fields_frame, height=4, width=25, font=('Arial', 10))
        addr_text.grid(row=len(fields), column=1, sticky='ew', pady=5, padx=(10, 0))
        
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # Кнопки
        buttons_frame = tk.Frame(dialog, bg='white')
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        def save_customer():
            # Проверяем заполнение обязательных полей
            if not entries["Название:"].get():
                messagebox.showerror("Ошибка", "Заполните название клиента!")
                return
                
            # Добавляем клиента
            self.db.add_customer(
                entries["Название:"].get(),
                entries["Email:"].get(),
                entries["Телефон:"].get(),
                addr_text.get("1.0", tk.END).strip()
            )
            
            messagebox.showinfo("Успех", "Клиент успешно добавлен!")
            dialog.destroy()
            self.load_customers()
                
        def cancel():
            dialog.destroy()
            
        save_btn = tk.Button(
            buttons_frame,
            text="Сохранить",
            command=save_customer,
            bg='#e67e22',
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
        
    def delete_selected_customer(self):
        """Удалить выбранного клиента"""
        selected_item = self.customers_tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите клиента для удаления!")
            return
            
        # Получаем данные выбранного клиента
        customer_data = self.customers_tree.item(selected_item[0])['values']
        customer_id = customer_data[0]
        customer_name = customer_data[1]
        
        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить клиента '{customer_name}'?"):
            self.db.delete_customer(customer_id)
            messagebox.showinfo("Успех", "Клиент успешно удален!")
            self.load_customers() 