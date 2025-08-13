#!/usr/bin/env python3
"""
Скрипт для проверки настройки CoinMarketCap API ключа
"""

import os
import sys
from pathlib import Path

def check_api_key():
    """Проверка настройки API ключа"""
    
    print("🔍 Проверка настройки CoinMarketCap API ключа...")
    print()
    
    # Проверяем наличие файла .env
    env_file = Path("backend/.env")
    if not env_file.exists():
        print("❌ Файл backend/.env не найден!")
        print()
        print("📝 Для создания файла .env выполните:")
        print("   cp backend/env.example backend/.env")
        print()
        return False
    
    print("✅ Файл backend/.env найден")
    
    # Проверяем содержимое .env
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'COINMARKETCAP_API_KEY=your_api_key_here' in content:
            print("❌ API ключ не настроен!")
            print()
            print("📝 Для настройки API ключа:")
            print("   1. Откройте файл backend/.env")
            print("   2. Замените 'your_api_key_here' на ваш реальный ключ")
            print("   3. Сохраните файл")
            print()
            return False
            
        if 'COINMARKETCAP_API_KEY=' in content:
            print("✅ API ключ настроен")
            return True
        else:
            print("❌ Переменная COINMARKETCAP_API_KEY не найдена в .env")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка чтения файла .env: {e}")
        return False

def main():
    """Основная функция"""
    print("=" * 50)
    print("🔑 Проверка CoinMarketCap API ключа")
    print("=" * 50)
    print()
    
    if check_api_key():
        print("🎉 API ключ настроен правильно!")
        print()
        print("🚀 Теперь можно запускать API:")
        print("   cd backend")
        print("   python main.py")
    else:
        print("⚠️ API ключ не настроен!")
        print()
        print("📚 Подробная инструкция в файле backend/SETUP.md")
    
    print()
    print("=" * 50)

if __name__ == "__main__":
    main() 