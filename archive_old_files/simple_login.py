#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упрощенный модуль авторизации ERP системы
"""

import tkinter as tk
from tkinter import messagebox
from database import Database

def simple_login_test():
    """Простой тест логина"""
    try:
        # Создаём базу данных
        db = Database()
        
        # Проверяем пользователей
        users = db.get_all_users()
        print(f"Найдено пользователей: {len(users)}")
        
        # Создаём простое окно авторизации
        root = tk.Tk()
        root.title("Простой вход в ERP")
        root.geometry("350x250")
        
        # Заголовок
        title = tk.Label(root, text="ERP Система - Вход", font=('Arial', 14, 'bold'))
        title.pack(pady=20)
        
        # Поля ввода
        login_frame = tk.Frame(root)
        login_frame.pack(pady=20)
        
        tk.Label(login_frame, text="Логин:").grid(row=0, column=0, padx=5, pady=5)
        login_entry = tk.Entry(login_frame)
        login_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(login_frame, text="Пароль:").grid(row=1, column=0, padx=5, pady=5)
        password_entry = tk.Entry(login_frame, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Кнопка входа
        def check_login():
            username = login_entry.get()
            password = password_entry.get()
            
            # Простая проверка
            if username == "admin" and password == "admin123":
                messagebox.showinfo("Успех", "Вход выполнен успешно!")
                root.destroy()
            elif username == "manager" and password == "manager123":
                messagebox.showinfo("Успех", "Менеджер вошёл в систему!")
                root.destroy()
            elif username == "operator" and password == "operator123":
                messagebox.showinfo("Успех", "Оператор вошёл в систему!")
                root.destroy()
            else:
                messagebox.showerror("Ошибка", "Неверные данные!")
                
        login_btn = tk.Button(root, text="Войти", command=check_login, bg='green', fg='white')
        login_btn.pack(pady=10)
        
        # Справка
        help_text = "Тестовые данные:\nadmin/admin123\nmanager/manager123\noperator/operator123"
        help_label = tk.Label(root, text=help_text, font=('Arial', 8), justify='left')
        help_label.pack(pady=10)
        
        # Запускаем
        root.mainloop()
        print("Окно авторизации закрыто")
        return True
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Тестирование простого окна авторизации...")
    if simple_login_test():
        print("✅ Тест прошёл успешно!")
    else:
        print("❌ Тест провален!") 