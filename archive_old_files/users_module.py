# -*- coding: utf-8 -*-
"""
Модуль управления пользователями ERP системы
"""

import tkinter as tk
from tkinter import ttk, messagebox

class UsersModule:
    def __init__(self, parent_frame, database):
        self.parent = parent_frame
        self.db = database
        self.create_widgets()
        self.load_users()
        
    def create_widgets(self):
        # Заголовок модуля
        title_label = tk.Label(
            self.parent,
            text="УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ",
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
            text="➕ Добавить пользователя",
            command=self.show_add_user_dialog,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            cursor='hand2'
        )
        add_btn.pack(side='left', padx=(0, 10))
        
        delete_btn = tk.Button(
            buttons_frame,
            text="🗑️ Удалить пользователя",
            command=self.delete_selected_user,
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
            command=self.load_users,
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
        
        # Создаем таблицу пользователей
        columns = ('ID', 'Логин', 'Полное имя', 'Роль', 'Email', 'Дата создания')
        self.users_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Настраиваем колонки
        self.users_tree.heading('ID', text='ID')
        self.users_tree.heading('Логин', text='Логин')
        self.users_tree.heading('Полное имя', text='Полное имя')
        self.users_tree.heading('Роль', text='Роль')
        self.users_tree.heading('Email', text='Email')
        self.users_tree.heading('Дата создания', text='Дата создания')
        
        # Настраиваем ширину колонок
        self.users_tree.column('ID', width=50)
        self.users_tree.column('Логин', width=100)
        self.users_tree.column('Полное имя', width=150)
        self.users_tree.column('Роль', width=100)
        self.users_tree.column('Email', width=150)
        self.users_tree.column('Дата создания', width=120)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем элементы
        self.users_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def load_users(self):
        """Загрузить список пользователей"""
        # Очищаем таблицу
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
            
        # Загружаем пользователей из базы данных
        users = self.db.get_all_users()
        for user in users:
            # user = (id, username, password, full_name, role, email, created_date)
            self.users_tree.insert('', 'end', values=(
                user[0], user[1], user[3], user[4], user[5], user[6]
            ))
            
    def show_add_user_dialog(self):
        """Показать диалог добавления пользователя"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Добавить пользователя")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.configure(bg='white')
        
        # Центрируем диалог
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        # Заголовок
        title_label = tk.Label(
            dialog,
            text="Добавление нового пользователя",
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
            ("Логин:", tk.StringVar()),
            ("Пароль:", tk.StringVar()),
            ("Полное имя:", tk.StringVar()),
            ("Email:", tk.StringVar())
        ]
        
        entries = {}
        for i, (label_text, var) in enumerate(fields):
            label = tk.Label(fields_frame, text=label_text, bg='white', font=('Arial', 10))
            label.grid(row=i, column=0, sticky='w', pady=5)
            
            entry = tk.Entry(fields_frame, textvariable=var, font=('Arial', 10), width=25)
            if label_text == "Пароль:":
                entry.config(show="*")
            entry.grid(row=i, column=1, sticky='ew', pady=5, padx=(10, 0))
            entries[label_text] = var
            
        # Роль
        role_label = tk.Label(fields_frame, text="Роль:", bg='white', font=('Arial', 10))
        role_label.grid(row=len(fields), column=0, sticky='w', pady=5)
        
        role_var = tk.StringVar(value="Оператор")
        role_combo = ttk.Combobox(
            fields_frame, 
            textvariable=role_var,
            values=["Администратор", "Менеджер", "Оператор"],
            state="readonly",
            width=22
        )
        role_combo.grid(row=len(fields), column=1, sticky='ew', pady=5, padx=(10, 0))
        
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # Кнопки
        buttons_frame = tk.Frame(dialog, bg='white')
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        def save_user():
            # Проверяем заполнение обязательных полей
            if not entries["Логин:"].get() or not entries["Пароль:"].get() or not entries["Полное имя:"].get():
                messagebox.showerror("Ошибка", "Заполните все обязательные поля!")
                return
                
            # Добавляем пользователя
            success = self.db.add_user(
                entries["Логин:"].get(),
                entries["Пароль:"].get(),
                entries["Полное имя:"].get(),
                role_var.get(),
                entries["Email:"].get()
            )
            
            if success:
                messagebox.showinfo("Успех", "Пользователь успешно добавлен!")
                dialog.destroy()
                self.load_users()
            else:
                messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует!")
                
        def cancel():
            dialog.destroy()
            
        save_btn = tk.Button(
            buttons_frame,
            text="Сохранить",
            command=save_user,
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
        
    def delete_selected_user(self):
        """Удалить выбранного пользователя"""
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите пользователя для удаления!")
            return
            
        # Получаем данные выбранного пользователя
        user_data = self.users_tree.item(selected_item[0])['values']
        user_id = user_data[0]
        username = user_data[1]
        
        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить пользователя '{username}'?"):
            self.db.delete_user(user_id)
            messagebox.showinfo("Успех", "Пользователь успешно удален!")
            self.load_users() 