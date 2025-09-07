"""
Тесты для API эндпоинтов
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
import json

from src.models import EducationLevel, TopicStatus, VKRTopic


class TestAPIEndpoints:
    """Тесты для API эндпоинтов"""
    
    def test_root_endpoint(self, test_client):
        """Тест корневого эндпоинта"""
        response = test_client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "VKR Topic Generator API"
        assert data["version"] == "0.1.0"
        assert data["status"] == "running"
    
    def test_health_check(self, test_client):
        """Тест проверки здоровья сервиса"""
        response = test_client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "model" in data
    
    def test_get_supported_fields(self, test_client):
        """Тест получения поддерживаемых областей"""
        response = test_client.get("/fields")
        assert response.status_code == 200
        
        data = response.json()
        assert "fields" in data
        assert "levels" in data
        assert isinstance(data["fields"], list)
        assert isinstance(data["levels"], list)
    
    @patch('src.api.server.topic_agent')
    def test_generate_topics_success(self, mock_agent, test_client, sample_topics_list):
        """Тест успешной генерации тем"""
        # Настройка мока
        mock_topics = [VKRTopic(**topic_data) for topic_data in sample_topics_list]
        mock_agent.generate_topics.return_value = mock_topics
        
        # Данные запроса
        request_data = {
            "field": "Информатика",
            "count": 2,
            "level": "Бакалавриат",
            "include_trends": True,
            "include_methodology": True
        }
        
        # Выполнение запроса
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
    
    def test_generate_topics_validation_error(self, test_client):
        """Тест валидации запроса генерации тем"""
        # Невалидные данные (отсутствует обязательное поле)
        request_data = {
            "count": 5,
            "level": "Бакалавриат"
            # Отсутствует поле "field"
        }
        
        response = test_client.post("/generate-topics", json=request_data)
        assert response.status_code == 422  # Validation Error
    
    def test_generate_topics_invalid_count(self, test_client):
        """Тест валидации количества тем"""
        request_data = {
            "field": "Информатика",
            "count": 25,  # Больше максимального значения
            "level": "Бакалавриат"
        }
        
        response = test_client.post("/generate-topics", json=request_data)
        assert response.status_code == 422
    
    @patch('src.api.server.get_db')
    def test_search_topics_success(self, mock_get_db, test_client, topic_repository, sample_topics_list):
        """Тест успешного поиска тем"""
        # Настройка мока репозитория
        mock_topics = [VKRTopic(**topic_data) for topic_data in sample_topics_list]
        topic_repository.search_topics = AsyncMock(return_value=(mock_topics, 2))
        mock_get_db.return_value = topic_repository
        
        # Параметры поиска
        params = {
            "query": "машинное обучение",
            "limit": 10,
            "offset": 0
        }
        
        # Выполнение запроса
        response = test_client.get("/topics", params=params)
        
        # Проверки
        assert response.status_code == 200
        data = response.json()
        assert "topics" in data
        assert "total_count" in data
        assert "page" in data
        assert "per_page" in data
        assert "has_next" in data
        assert "has_prev" in data
        assert len(data["topics"]) == 2
        assert data["total_count"] == 2
    
    def test_search_topics_validation_error(self, test_client):
        """Тест валидации поиска тем"""
        # Отсутствует обязательный параметр query
        params = {
            "limit": 10
        }
        
        response = test_client.get("/topics", params=params)
        assert response.status_code == 422
    
    @patch('src.api.server.get_db')
    def test_get_topic_success(self, mock_get_db, test_client, topic_repository, sample_topic_data):
        """Тест успешного получения темы по ID"""
        # Настройка мока
        mock_topic = VKRTopic(**sample_topic_data)
        topic_repository.get_topic = AsyncMock(return_value=mock_topic)
        mock_get_db.return_value = topic_repository
        
        # Выполнение запроса
        response = test_client.get("/topics/1")
        
        # Проверки
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == sample_topic_data["title"]
        assert data["field"] == sample_topic_data["field"]
        assert data["level"] == sample_topic_data["level"]
    
    @patch('src.api.server.get_db')
    def test_get_topic_not_found(self, mock_get_db, test_client, topic_repository):
        """Тест получения несуществующей темы"""
        # Настройка мока для возврата None
        topic_repository.get_topic = AsyncMock(return_value=None)
        mock_get_db.return_value = topic_repository
        
        # Выполнение запроса
        response = test_client.get("/topics/999")
        
        # Проверки
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Тема не найдена"
    
    @patch('src.api.server.get_db')
    def test_update_topic_success(self, mock_get_db, test_client, topic_repository, sample_topic_data):
        """Тест успешного обновления темы"""
        # Настройка мока
        updated_topic = VKRTopic(**sample_topic_data)
        updated_topic.title = "Обновленное название"
        topic_repository.update_topic = AsyncMock(return_value=updated_topic)
        mock_get_db.return_value = topic_repository
        
        # Данные для обновления
        update_data = {
            "title": "Обновленное название",
            "description": "Обновленное описание"
        }
        
        # Выполнение запроса
        response = test_client.put("/topics/1", json=update_data)
        
        # Проверки
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Обновленное название"
    
    @patch('src.api.server.get_db')
    def test_delete_topic_success(self, mock_get_db, test_client, topic_repository):
        """Тест успешного удаления темы"""
        # Настройка мока
        topic_repository.delete_topic = AsyncMock(return_value=True)
        mock_get_db.return_value = topic_repository
        
        # Выполнение запроса
        response = test_client.delete("/topics/1")
        
        # Проверки
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Тема успешно удалена"
    
    @patch('src.api.server.get_db')
    def test_delete_topic_not_found(self, mock_get_db, test_client, topic_repository):
        """Тест удаления несуществующей темы"""
        # Настройка мока для возврата False
        topic_repository.delete_topic = AsyncMock(return_value=False)
        mock_get_db.return_value = topic_repository
        
        # Выполнение запроса
        response = test_client.delete("/topics/999")
        
        # Проверки
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Тема не найдена"
    
    @patch('src.api.server.get_db')
    def test_get_stats_success(self, mock_get_db, test_client, topic_repository):
        """Тест получения статистики"""
        # Настройка мока
        mock_stats = {
            "total_topics": 100,
            "by_field": {"Информатика": 50, "Экономика": 30, "Медицина": 20},
            "by_level": {"Бакалавриат": 60, "Магистратура": 40},
            "by_status": {"DRAFT": 80, "APPROVED": 20},
            "avg_relevance_score": 0.85,
            "most_popular_keywords": []
        }
        topic_repository.get_stats = AsyncMock(return_value=mock_stats)
        mock_get_db.return_value = topic_repository
        
        # Выполнение запроса
        response = test_client.get("/stats")
        
        # Проверки
        assert response.status_code == 200
        data = response.json()
        assert data["total_topics"] == 100
        assert "by_field" in data
        assert "by_level" in data
        assert "by_status" in data


class TestAPIErrorHandling:
    """Тесты обработки ошибок API"""
    
    @patch('src.api.server.topic_agent')
    def test_generate_topics_internal_error(self, mock_agent, test_client):
        """Тест обработки внутренней ошибки при генерации тем"""
        # Настройка мока для выброса исключения
        mock_agent.generate_topics.side_effect = Exception("Internal error")
        
        request_data = {
            "field": "Информатика",
            "count": 5
        }
        
        response = test_client.post("/generate-topics", json=request_data)
        assert response.status_code == 500
        data = response.json()
        assert "Internal error" in data["detail"]
    
    @patch('src.api.server.get_db')
    def test_search_topics_database_error(self, mock_get_db, test_client, topic_repository):
        """Тест обработки ошибки базы данных при поиске"""
        # Настройка мока для выброса исключения
        topic_repository.search_topics = AsyncMock(side_effect=Exception("Database error"))
        mock_get_db.return_value = topic_repository
        
        params = {"query": "test"}
        response = test_client.get("/topics", params=params)
        assert response.status_code == 500
        data = response.json()
        assert "Database error" in data["detail"]
