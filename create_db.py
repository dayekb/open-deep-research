#!/usr/bin/env python3
"""
Создание базы данных
"""

import asyncio
import sys
from pathlib import Path

# Добавляем путь к src
sys.path.append(str(Path(__file__).parent / "src"))

from src.database.models import Base
from src.database.repository import get_db
from sqlalchemy import create_engine
from src.config.settings import settings


async def create_database():
    """Создание базы данных"""
    print("🗄️ СОЗДАНИЕ БАЗЫ ДАННЫХ")
    print("=" * 40)
    
    try:
        # Создаем движок
        engine = create_engine(settings.database_url)
        
        # Создаем все таблицы
        print("Создаем таблицы...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ База данных создана!")
        print(f"Файл: {settings.database_url}")
        
        # Тестируем подключение
        print("\nТестируем подключение...")
        async with get_db() as db:
            print("✅ Подключение работает!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(create_database())
