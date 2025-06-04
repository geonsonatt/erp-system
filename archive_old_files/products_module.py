# -*- coding: utf-8 -*-
"""
Модуль управления товарами ERP системы
"""

import tkinter as tk
from tkinter import ttk, messagebox

class ProductsModule:
    def __init__(self, parent_frame, database):
        self.parent = parent_frame
        self.db = database
        self.create_widgets()
        self.load_products()
        
    def create_widgets(self):
        # Заголовок модуля
        title_label = tk.Label(
            self.parent,
            text="УПРАВЛЕНИЕ ТОВАРАМИ",
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
            text="📦 Добавить товар",
            command=self.show_add_product_dialog,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            cursor='hand2'
        )
        add_btn.pack(side='left', padx=(0, 10))
        
        delete_btn = tk.Button(
            buttons_frame,
            text="🗑️ Удалить товар",
            command=self.delete_selected_product,
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
            command=self.load_products,
            bg='#3498db',
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
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', self.filter_products)
        
        # Фрейм для таблицы
        table_frame = tk.Frame(self.parent, bg='white')
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Создаем таблицу товаров
        columns = ('ID', 'Название', 'Описание', 'Цена', 'Количество', 'Категория', 'Дата создания')
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Настраиваем колонки
        self.products_tree.heading('ID', text='ID')
        self.products_tree.heading('Название', text='Название')
        self.products_tree.heading('Описание', text='Описание')
        self.products_tree.heading('Цена', text='Цена (₽)')
        self.products_tree.heading('Количество', text='Кол-во')
        self.products_tree.heading('Категория', text='Категория')
        self.products_tree.heading('Дата создания', text='Дата создания')
        
        # Настраиваем ширину колонок
        self.products_tree.column('ID', width=50)
        self.products_tree.column('Название', width=150)
        self.products_tree.column('Описание', width=200)
        self.products_tree.column('Цена', width=100)
        self.products_tree.column('Количество', width=80)
        self.products_tree.column('Категория', width=120)
        self.products_tree.column('Дата создания', width=120)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем элементы
        self.products_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def load_products(self):
        """Загрузить список товаров"""
        # Очищаем таблицу
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
            
        # Загружаем товары из базы данных
        products = self.db.get_all_products()
        for product in products:
            # product = (id, name, description, price, quantity, category, created_date)
            self.products_tree.insert('', 'end', values=(
                product[0], product[1], product[2], f"{product[3]:.2f}", 
                product[4], product[5], product[6]
            ))
            
    def show_add_product_dialog(self):
        """Показать диалог добавления товара"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Добавить товар")
        dialog.geometry("450x350")
        dialog.resizable(False, False)
        dialog.configure(bg='white')
        
        # Центрируем диалог
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        # Заголовок
        title_label = tk.Label(
            dialog,
            text="Добавление нового товара",
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
            ("Цена (₽):", tk.StringVar()),
            ("Количество:", tk.StringVar())
        ]
        
        entries = {}
        for i, (label_text, var) in enumerate(fields):
            label = tk.Label(fields_frame, text=label_text, bg='white', font=('Arial', 10))
            label.grid(row=i, column=0, sticky='w', pady=5)
            
            entry = tk.Entry(fields_frame, textvariable=var, font=('Arial', 10), width=25)
            entry.grid(row=i, column=1, sticky='ew', pady=5, padx=(10, 0))
            entries[label_text] = var
            
        # Описание
        desc_label = tk.Label(fields_frame, text="Описание:", bg='white', font=('Arial', 10))
        desc_label.grid(row=len(fields), column=0, sticky='nw', pady=5)
        
        desc_text = tk.Text(fields_frame, height=4, width=25, font=('Arial', 10))
        desc_text.grid(row=len(fields), column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Категория
        cat_label = tk.Label(fields_frame, text="Категория:", bg='white', font=('Arial', 10))
        cat_label.grid(row=len(fields)+1, column=0, sticky='w', pady=5)
        
        cat_var = tk.StringVar(value="Общие")
        cat_combo = ttk.Combobox(
            fields_frame, 
            textvariable=cat_var,
            values=["Электроника", "Аксессуары", "Оргтехника", "Мебель", "Канцтовары", "Общие"],
            width=22
        )
        cat_combo.grid(row=len(fields)+1, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # Кнопки
        buttons_frame = tk.Frame(dialog, bg='white')
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        def save_product():
            # Проверяем заполнение обязательных полей
            if not entries["Название:"].get() or not entries["Цена (₽):"].get() or not entries["Количество:"].get():
                messagebox.showerror("Ошибка", "Заполните все обязательные поля!")
                return
                
            try:
                price = float(entries["Цена (₽):"].get())
                quantity = int(entries["Количество:"].get())
                
                if price < 0 or quantity < 0:
                    messagebox.showerror("Ошибка", "Цена и количество должны быть положительными!")
                    return
                    
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат цены или количества!")
                return
                
            # Добавляем товар
            self.db.add_product(
                entries["Название:"].get(),
                desc_text.get("1.0", tk.END).strip(),
                price,
                quantity,
                cat_var.get()
            )
            
            messagebox.showinfo("Успех", "Товар успешно добавлен!")
            dialog.destroy()
            self.load_products()
                
        def cancel():
            dialog.destroy()
            
        save_btn = tk.Button(
            buttons_frame,
            text="Сохранить",
            command=save_product,
            bg='#27ae60',
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
        
    def delete_selected_product(self):
        """Удалить выбранный товар"""
        selected_item = self.products_tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите товар для удаления!")
            return
            
        # Получаем данные выбранного товара
        product_data = self.products_tree.item(selected_item[0])['values']
        product_id = product_data[0]
        product_name = product_data[1]
        
        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить товар '{product_name}'?"):
            self.db.delete_product(product_id)
            messagebox.showinfo("Успех", "Товар успешно удален!")
            self.load_products() 

    def filter_products(self, event=None):
        """Фильтрация товаров по поиску"""
        query = self.search_var.get().lower()
        
        # Очищаем таблицу
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
            
        # Загружаем все товары
        products = self.db.get_all_products()
        
        # Фильтруем и отображаем
        for product in products:
            if (query in product[1].lower() or  # название
                query in (product[2] or '').lower() or  # описание
                query in (product[5] or '').lower()):  # категория
                self.products_tree.insert('', 'end', values=(
                    product[0], product[1], product[2], f"{product[3]:.2f}", 
                    product[4], product[5], product[6]
                )) 