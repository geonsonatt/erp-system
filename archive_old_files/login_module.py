# -*- coding: utf-8 -*-
"""
Модуль авторизации ERP системы
"""

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib

class LoginWindow:
    def __init__(self, database, callback):
        self.db = database
        self.callback = callback
        self.current_user = None
        self.root = tk.Tk()
        self.root.title("Вход в ERP систему")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # Центрируем окно
        self.center_window()
        
        self.create_widgets()
        
    def center_window(self):
        """Центрировать окно на экране"""
        # Упрощенная версия без проблемных вызовов
        try:
            self.root.update_idletasks()
            # Устанавливаем позицию без сложных вычислений
            self.root.geometry("400x300+200+200")
        except:
            # Если возникают проблемы, просто не центрируем
            pass
        
    def create_widgets(self):
        # Главный фрейм
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Логотип и заголовок
        title_label = tk.Label(
            main_frame,
            text="🏢 ERP СИСТЕМА",
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Авторизация пользователя",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Фрейм для формы
        form_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Заголовок формы
        form_title = tk.Label(
            form_frame,
            text="Вход в систему",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        form_title.pack(pady=15)
        
        # Поля ввода
        fields_frame = tk.Frame(form_frame, bg='white')
        fields_frame.pack(fill='x', padx=20, pady=10)
        
        # Логин
        login_label = tk.Label(
            fields_frame,
            text="Логин:",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        login_label.pack(anchor='w', pady=(5, 0))
        
        self.login_var = tk.StringVar()
        self.login_entry = tk.Entry(
            fields_frame,
            textvariable=self.login_var,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            width=25
        )
        self.login_entry.pack(pady=(5, 15), ipady=5)
        
        # Пароль
        password_label = tk.Label(
            fields_frame,
            text="Пароль:",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        password_label.pack(anchor='w', pady=(5, 0))
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            fields_frame,
            textvariable=self.password_var,
            font=('Arial', 12),
            show="*",
            relief='solid',
            bd=1,
            width=25
        )
        self.password_entry.pack(pady=(5, 20), ipady=5)
        
        # Кнопка входа
        login_btn = tk.Button(
            fields_frame,
            text="🔐 Войти в систему",
            command=self.authenticate_user,
            bg='#27ae60',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='flat',
            cursor='hand2',
            pady=8
        )
        login_btn.pack(pady=10, fill='x')
        
        # Информация о тестовых пользователях
        info_frame = tk.Frame(form_frame, bg='#ecf0f1', relief='sunken', bd=1)
        info_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        info_label = tk.Label(
            info_frame,
            text="💡 Тестовые пользователи:",
            font=('Arial', 9, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        info_label.pack(pady=(5, 0))
        
        users_info = [
            "admin / admin123 (Администратор)",
            "manager / manager123 (Менеджер)", 
            "operator / operator123 (Оператор)"
        ]
        
        for user_info in users_info:
            user_label = tk.Label(
                info_frame,
                text=user_info,
                font=('Arial', 8),
                bg='#ecf0f1',
                fg='#7f8c8d'
            )
            user_label.pack()
            
        tk.Label(info_frame, text="", bg='#ecf0f1').pack(pady=2)
        
        # Привязываем Enter к кнопке входа
        self.root.bind('<Return>', lambda e: self.authenticate_user())
        
        # Фокус на поле логина
        self.login_entry.focus()
        
    def hash_password(self, password):
        """Хешировать пароль"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def authenticate_user(self):
        """Аутентификация пользователя"""
        username = self.login_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return
            
        # Проверяем пользователя в базе данных
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, password, full_name, role, email 
            FROM users 
            WHERE username = ?
        """, (username,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user and user[2] == password:  # Простая проверка пароля (в реальной системе нужно хешировать)
            self.current_user = {
                'id': user[0],
                'username': user[1],
                'full_name': user[3],
                'role': user[4],
                'email': user[5]
            }
            
            # Логируем вход
            self.log_user_action("Вход в систему")
            
            messagebox.showinfo("Успех", f"Добро пожаловать, {user[3]}!")
            self.root.destroy()
            
            # Запускаем главное приложение
            self.callback(self.current_user)
            
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")
            self.password_var.set("")  # Очищаем поле пароля
            
    def log_user_action(self, action):
        """Логирование действий пользователя"""
        if self.current_user:
            import datetime
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Создаем таблицу логов если её нет
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    action TEXT,
                    timestamp TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            cursor.execute('''
                INSERT INTO user_logs (user_id, username, action, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (
                self.current_user['id'],
                self.current_user['username'],
                action,
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            
            conn.commit()
            conn.close()
            
    def run(self):
        """Запустить окно авторизации"""
        self.root.mainloop()
        return self.current_user 