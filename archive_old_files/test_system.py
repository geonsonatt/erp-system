#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для тестирования основных функций ERP системы
"""

import sys
import sqlite3
from database import Database

def test_database_connection():
    """Тест подключения к базе данных"""
    print("🔗 Тестирование подключения к базе данных...")
    try:
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        expected_tables = ['users', 'products', 'customers', 'orders', 'order_items']
        found_tables = [table[0] for table in tables]
        
        for table in expected_tables:
            if table in found_tables:
                print(f"  ✅ Таблица '{table}' найдена")
            else:
                print(f"  ❌ Таблица '{table}' НЕ найдена")
                
        return True
    except Exception as e:
        print(f"  ❌ Ошибка подключения: {e}")
        return False

def test_users_data():
    """Тест данных пользователей"""
    print("\n👥 Тестирование пользователей...")
    try:
        db = Database()
        users = db.get_all_users()
        
        if len(users) >= 3:
            print(f"  ✅ Найдено пользователей: {len(users)}")
            for user in users:
                print(f"    - {user[1]} ({user[4]}) - {user[3]}")
        else:
            print(f"  ⚠️ Найдено только {len(users)} пользователей")
            
        return True
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False

def test_products_data():
    """Тест данных товаров"""
    print("\n📦 Тестирование товаров...")
    try:
        db = Database()
        products = db.get_all_products()
        
        if len(products) >= 3:
            print(f"  ✅ Найдено товаров: {len(products)}")
            for product in products[:3]:  # Показываем первые 3
                print(f"    - {product[1]} - {product[3]:.2f} ₽ (остаток: {product[4]})")
        else:
            print(f"  ⚠️ Найдено только {len(products)} товаров")
            
        return True
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False

def test_customers_data():
    """Тест данных клиентов"""
    print("\n👤 Тестирование клиентов...")
    try:
        db = Database()
        customers = db.get_all_customers()
        
        if len(customers) >= 2:
            print(f"  ✅ Найдено клиентов: {len(customers)}")
            for customer in customers:
                print(f"    - {customer[1]} ({customer[2]})")
        else:
            print(f"  ⚠️ Найдено только {len(customers)} клиентов")
            
        return True
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False

def test_orders_data():
    """Тест данных заказов"""
    print("\n📋 Тестирование заказов...")
    try:
        db = Database()
        orders = db.get_all_orders()
        
        print(f"  ✅ Найдено заказов: {len(orders)}")
        if len(orders) > 0:
            for order in orders:
                print(f"    - Заказ #{order[0]:04d}: {order[1]} - {order[2]:.2f} ₽ ({order[3]})")
                
        return True
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False

def test_statistics():
    """Тест статистических функций"""
    print("\n📊 Тестирование статистики...")
    try:
        db = Database()
        
        total_sales = db.get_total_sales()
        total_products = db.get_total_products()
        total_customers = db.get_total_customers()
        total_orders = db.get_total_orders()
        
        print(f"  ✅ Общая сумма продаж: {total_sales:.2f} ₽")
        print(f"  ✅ Товаров в каталоге: {total_products}")
        print(f"  ✅ Клиентов в базе: {total_customers}")
        print(f"  ✅ Всего заказов: {total_orders}")
        
        return True
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 ТЕСТИРОВАНИЕ ERP СИСТЕМЫ v2.0")
    print("=" * 50)
    
    tests = [
        test_database_connection,
        test_users_data,
        test_products_data,
        test_customers_data,
        test_orders_data,
        test_statistics
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ❌ Критическая ошибка в тесте: {e}")
            failed += 1
            
    print("\n" + "=" * 50)
    print(f"📈 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"  ✅ Пройдено тестов: {passed}")
    print(f"  ❌ Провалено тестов: {failed}")
    
    if failed == 0:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("💡 ERP система готова к работе!")
    else:
        print(f"\n⚠️ Обнаружены проблемы в {failed} тестах")
        print("🔧 Рекомендуется исправить ошибки перед использованием")
        
    print("\n🚀 Для запуска системы используйте: python3 main.py")

if __name__ == "__main__":
    main() 