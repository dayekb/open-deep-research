"""
Главный файл для запуска сервиса генерации тем ВКР
"""

import uvicorn
from src.config import settings
from src.database.models import Base
from sqlalchemy import create_engine


def create_tables():
    """Создание таблиц в базе данных"""
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы базы данных созданы")


def main():
    """Запуск сервера"""
    print("🚀 Запуск сервиса генерации тем ВКР")
    print(f"📊 Модель: {settings.default_model}")
    print(f"🔍 Поиск: {settings.default_search_api}")
    print(f"🌐 Сервер: http://{settings.host}:{settings.port}")
    print(f"📚 Документация: http://{settings.host}:{settings.port}/docs")
    
    # Создание таблиц
    create_tables()
    
    # Запуск сервера
    uvicorn.run(
        "src.api.server:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )


if __name__ == "__main__":
    main()
