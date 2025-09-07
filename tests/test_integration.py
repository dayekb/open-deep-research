"""
Интеграционные тесты
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock

from src.api.server import app
from src.agents import VKRTopicAgent
from src.models import EducationLevel


class TestIntegration:
    """Интеграционные тесты"""
    
    @pytest.mark.asyncio
    async def test_full_generation_flow(self, test_client):
        """Тест полного потока генерации тем"""
        # Мокаем агент для контролируемого тестирования
        mock_topics = [
            {
                "title": "Интеграционная тема 1",
                "field": "Информатика",
                "level": "Бакалавриат",
                "description": "Описание интеграционной темы",
                "keywords": ["интеграция", "тест"],
                "methodology": "Интеграционное тестирование",
                "expected_results": "Успешная интеграция"
            },
            {
                "title": "Интеграционная тема 2", 
                "field": "Информатика",
                "level": "Бакалавриат",
                "description": "Описание второй темы",
                "keywords": ["система", "тест"],
                "methodology": "Системное тестирование",
                "expected_results": "Рабочая система"
            }
        ]
        
        with patch('src.api.server.topic_agent') as mock_agent:
            # Настройка мока агента
            mock_agent.generate_topics.return_value = [
                type('VKRTopic', (), topic) for topic in mock_topics
            ]
            
            # Запрос на генерацию тем
            request_data = {
                "field": "Информатика",
                "count": 2,
                "level": "Бакалавриат",
                "include_trends": True,
                "include_methodology": True
            }
            
            response = test_client.post("/generate-topics", json=request_data)
            
            # Проверки
            assert response.status_code == 200
            data = response.json()
            
            assert "topics" in data
            assert "total_count" in data
            assert "generation_time" in data
            assert "model_used" in data
            
            assert len(data["topics"]) == 2
            assert data["total_count"] == 2
            assert data["model_used"] == "openai:gpt-4.1"
            
            # Проверяем структуру тем
            for topic in data["topics"]:
                assert "title" in topic
                assert "field" in topic
                assert "level" in topic
                assert "description" in topic
                assert "keywords" in topic
    
    @pytest.mark.asyncio
    async def test_generation_and_search_flow(self, test_client, topic_repository):
        """Тест потока генерации и поиска тем"""
        # Мокаем агент
        mock_topics = [
            type('VKRTopic', (), {
                "title": "Тема для поиска",
                "field": "Информатика",
                "level": "Бакалавриат",
                "description": "Описание темы для поиска",
                "keywords": ["поиск", "тест"],
                "methodology": "Поисковое тестирование",
                "expected_results": "Найденные результаты"
            })
        ]
        
        with patch('src.api.server.topic_agent') as mock_agent:
            mock_agent.generate_topics.return_value = mock_topics
            
            # 1. Генерируем темы
            request_data = {
                "field": "Информатика",
                "count": 1,
                "level": "Бакалавриат"
            }
            
            response = test_client.post("/generate-topics", json=request_data)
            assert response.status_code == 200
            
            # 2. Ищем сгенерированные темы
            search_params = {
                "query": "поиск",
                "limit": 10
            }
            
            response = test_client.get("/topics", params=search_params)
            assert response.status_code == 200
            
            data = response.json()
            assert "topics" in data
            assert "total_count" in data
    
    @pytest.mark.asyncio
    async def test_error_handling_flow(self, test_client):
        """Тест обработки ошибок в полном потоке"""
        with patch('src.api.server.topic_agent') as mock_agent:
            # Настройка мока для выброса исключения
            mock_agent.generate_topics.side_effect = Exception("Тестовая ошибка")
            
            request_data = {
                "field": "Информатика",
                "count": 1
            }
            
            response = test_client.post("/generate-topics", json=request_data)
            
            # Проверяем, что ошибка обработана корректно
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
            assert "Тестовая ошибка" in data["detail"]
    
    def test_api_documentation(self, test_client):
        """Тест доступности документации API"""
        # Проверяем Swagger UI
        response = test_client.get("/docs")
        assert response.status_code == 200
        
        # Проверяем ReDoc
        response = test_client.get("/redoc")
        assert response.status_code == 200
        
        # Проверяем OpenAPI схему
        response = test_client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_data = response.json()
        assert "openapi" in openapi_data
        assert "info" in openapi_data
        assert "paths" in openapi_data
    
    def test_cors_headers(self, test_client):
        """Тест CORS заголовков"""
        response = test_client.options("/generate-topics")
        
        # Проверяем, что CORS заголовки присутствуют
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, test_client):
        """Тест параллельных запросов"""
        import asyncio
        import aiohttp
        
        async def make_request(session, url, data):
            async with session.post(url, json=data) as response:
                return await response.json()
        
        async def test_concurrent():
            async with aiohttp.ClientSession() as session:
                # Создаем несколько задач
                tasks = []
                for i in range(5):
                    data = {
                        "field": f"Область {i}",
                        "count": 1,
                        "level": "Бакалавриат"
                    }
                    task = make_request(session, "http://testserver/generate-topics", data)
                    tasks.append(task)
                
                # Выполняем параллельно
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Проверяем результаты
                successful = [r for r in results if not isinstance(r, Exception)]
                assert len(successful) >= 3  # Не менее 60% успешных запросов
        
        # Запускаем тест (требует aiohttp)
        try:
            asyncio.run(test_concurrent())
        except ImportError:
            pytest.skip("aiohttp не установлен")
    
    def test_data_validation_flow(self, test_client):
        """Тест валидации данных в полном потоке"""
        # Тестируем различные невалидные запросы
        invalid_requests = [
            # Отсутствует обязательное поле
            {"count": 5},
            # Невалидное количество тем
            {"field": "Информатика", "count": 0},
            {"field": "Информатика", "count": 25},
            # Невалидный уровень образования
            {"field": "Информатика", "count": 5, "level": "Несуществующий уровень"},
            # Невалидная оценка релевантности
            {"field": "Информатика", "count": 5, "min_relevance_score": 1.5}
        ]
        
        for invalid_request in invalid_requests:
            response = test_client.post("/generate-topics", json=invalid_request)
            assert response.status_code == 422  # Validation Error
            
            data = response.json()
            assert "detail" in data
    
    @pytest.mark.asyncio
    async def test_database_integration(self, test_client, topic_repository):
        """Тест интеграции с базой данных"""
        # Создаем тему через API
        mock_topics = [
            type('VKRTopic', (), {
                "title": "Тема для БД",
                "field": "Информатика",
                "level": "Бакалавриат",
                "description": "Описание темы для БД",
                "keywords": ["база", "данных"],
                "methodology": "Тестирование БД",
                "expected_results": "Сохранение в БД"
            })
        ]
        
        with patch('src.api.server.topic_agent') as mock_agent:
            mock_agent.generate_topics.return_value = mock_topics
            
            request_data = {
                "field": "Информатика",
                "count": 1,
                "level": "Бакалавриат"
            }
            
            response = test_client.post("/generate-topics", json=request_data)
            assert response.status_code == 200
            
            # Проверяем, что тема сохранилась в БД
            stats = await topic_repository.get_stats()
            assert stats.total_topics >= 1
            
            # Проверяем поиск в БД
            search_request = type('TopicSearchRequest', (), {
                "query": "база данных",
                "limit": 10,
                "offset": 0
            })()
            
            topics, total_count = await topic_repository.search_topics(search_request)
            assert total_count >= 1
