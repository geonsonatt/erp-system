#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простая ERP система для курсовой работы - упрощенная версия запуска
"""

import tkinter as tk
from tkinter import messagebox
import sys

# Импортируем модули нашей ERP системы
from database import Database
from login_module import LoginWindow

def test_simple_window():
    """Простой тест создания окна"""
    root = tk.Tk()
    root.title("Тест ERP системы")
    root.geometry("400x300")
    
    label = tk.Label(root, text="✅ ERP система работает!", font=('Arial', 16))
    label.pack(expand=True)
    
    def close_app():
        root.destroy()
    
    btn = tk.Button(root, text="Закрыть", command=close_app)
    btn.pack(pady=20)
    
    root.mainloop()

def test_database():
    """Тест базы данных"""
    try:
        db = Database()
        users = db.get_all_users()
        print(f"✅ База данных работает. Найдено пользователей: {len(users)}")
        return True
    except Exception as e:
        print(f"❌ Ошибка базы данных: {e}")
        return False

def test_login_window():
    """Тест окна логина"""
    try:
        db = Database()
        
        def success_callback(user):
            print(f"✅ Пользователь авторизован: {user['username']}")
            return user
            
        login_window = LoginWindow(db, success_callback)
        # Здесь просто создаём и не запускаем mainloop
        print("✅ Окно логина создано успешно")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания окна логина: {e}")
        return False

def main():
    print("🧪 ТЕСТИРОВАНИЕ ERP СИСТЕМЫ (упрощенная версия)")
    print("=" * 50)
    
    # Тест 1: База данных
    print("1. Тестирование базы данных...")
    if not test_database():
        return
    
    # Тест 2: Окно логина
    print("2. Тестирование создания окна логина...")
    if not test_login_window():
        return
    
    # Тест 3: Простое GUI окно
    print("3. Тестирование простого GUI...")
    print("   Открываю тестовое окно...")
    
    try:
        test_simple_window()
        print("✅ Все тесты пройдены успешно!")
    except Exception as e:
        print(f"❌ Ошибка GUI: {e}")

if __name__ == "__main__":
    main() 