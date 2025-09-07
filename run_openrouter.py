#!/usr/bin/env python3
"""
Запуск сервиса с OpenRouter API
"""

import os
import sys
from pathlib import Path

# Добавляем путь к src
sys.path.append(str(Path(__file__).parent / "src"))

def check_environment():
    """Проверка окружения"""
    print("🔍 Проверка окружения...")
    
    # Проверяем API ключ
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY не найден")
        print("Установите ключ:")
        print("  export OPENROUTER_API_KEY=your_key_here")
        print("  или создайте .env файл с OPENROUTER_API_KEY=your_key_here")
        return False
    
    print(f"✅ API ключ найден: {api_key[:10]}...")
    
    # Проверяем зависимости
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ Основные зависимости установлены")
    except ImportError as e:
        print(f"❌ Отсутствует зависимость: {e}")
        print("Установите: pip install -r requirements.txt")
        return False
    
    return True

def create_env_file():
    """Создание .env файла если его нет"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Создание .env файла...")
        
        api_key = input("Введите ваш OpenRouter API ключ: ").strip()
        if not api_key:
            print("❌ API ключ не введен")
            return False
        
        env_content = f"""# OpenRouter API
OPENROUTER_API_KEY={api_key}

# Настройки сервера
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Модель по умолчанию
DEFAULT_MODEL=openrouter:meta-llama/llama-3.1-8b-instruct:free

# База данных
DATABASE_URL=sqlite:///./vkr_topics.db
"""
        
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_content)
        
        print("✅ .env файл создан")
        return True
    
    return True

def main():
    """Основная функция"""
    print("🚀 ЗАПУСК СЕРВИСА ГЕНЕРАЦИИ ТЕМ ВКР С OPENROUTER")
    print("=" * 60)
    
    # Проверяем окружение
    if not check_environment():
        return 1
    
    # Создаем .env файл если нужно
    if not create_env_file():
        return 1
    
    print("\n🌐 Запуск сервера...")
    print("Сервер будет доступен по адресу: http://localhost:8000")
    print("Документация API: http://localhost:8000/docs")
    print("Нажмите Ctrl+C для остановки")
    print("-" * 60)
    
    try:
        # Импортируем и запускаем сервер
        from src.api.server import app
        import uvicorn
        
        uvicorn.run(
            "src.api.server:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Сервер остановлен")
        return 0
    except Exception as e:
        print(f"\n❌ Ошибка запуска: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
