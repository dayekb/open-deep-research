"""
Конфигурация pytest для тестов
"""

import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock

from src.api.server import app
from src.database.models import Base
from src.database.repository import TopicRepository
from src.config import settings


@pytest.fixture(scope="session")
def event_loop():
    """Создание event loop для асинхронных тестов"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_db():
    """Создание тестовой базы данных"""
    # Используем in-memory SQLite для тестов
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def topic_repository(test_db):
    """Создание репозитория для тестов"""
    return TopicRepository(test_db)


@pytest.fixture
def test_client():
    """Создание тестового клиента FastAPI"""
    return TestClient(app)


@pytest.fixture
def mock_llm():
    """Мок языковой модели"""
    mock = AsyncMock()
    mock.ainvoke.return_value = MagicMock()
    mock.ainvoke.return_value.content = """
    1. Разработка системы рекомендаций на основе машинного обучения
    Актуальность: Машинное обучение активно развивается и находит применение в различных областях.
    Ключевые слова: машинное обучение, рекомендательные системы, алгоритмы
    Методология: Разработка и тестирование алгоритмов машинного обучения
    Ожидаемые результаты: Функциональная система рекомендаций
    
    2. Анализ данных социальных сетей с использованием методов ИИ
    Актуальность: Социальные сети генерируют огромные объемы данных, требующих анализа.
    Ключевые слова: анализ данных, социальные сети, искусственный интеллект
    Методология: Сбор данных, предобработка, применение алгоритмов ИИ
    Ожидаемые результаты: Инструменты для анализа социальных данных
    """
    return mock


@pytest.fixture
def sample_topic_data():
    """Тестовые данные для тем"""
    return {
        "title": "Разработка системы рекомендаций на основе машинного обучения",
        "field": "Информатика",
        "specialization": "Машинное обучение",
        "level": "Бакалавриат",
        "description": "Исследование и разработка системы рекомендаций",
        "keywords": ["машинное обучение", "рекомендательные системы", "алгоритмы"],
        "methodology": "Разработка и тестирование алгоритмов",
        "expected_results": "Функциональная система рекомендаций"
    }


@pytest.fixture
def sample_topics_list():
    """Список тестовых тем"""
    return [
        {
            "title": "Разработка системы рекомендаций на основе машинного обучения",
            "field": "Информатика",
            "level": "Бакалавриат",
            "description": "Исследование и разработка системы рекомендаций",
            "keywords": ["машинное обучение", "рекомендательные системы"]
        },
        {
            "title": "Анализ данных социальных сетей с использованием методов ИИ",
            "field": "Информатика", 
            "level": "Магистратура",
            "description": "Анализ больших данных социальных сетей",
            "keywords": ["анализ данных", "социальные сети", "ИИ"]
        }
    ]
