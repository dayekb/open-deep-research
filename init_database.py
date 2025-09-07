#!/usr/bin/env python3
"""
Инициализация базы данных
"""

import asyncio
import sys
from pathlib import Path

# Добавляем путь к src
sys.path.append(str(Path(__file__).parent / "src"))

from src.database.connection import get_engine
from src.database.models import Base


async def init_database():
    """Инициализация базы данных"""
    print("🗄️ ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ")
    print("=" * 40)
    
    try:
        # Получаем движок
        engine = get_engine()
        
        # Создаем все таблицы
        print("Создаем таблицы...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ База данных инициализирована!")
        print("Таблицы созданы успешно")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(init_database())
