"""
Тесты для моделей данных
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from src.models import VKRTopic, TopicRequest, TopicResponse, EducationLevel, TopicStatus


class TestVKRTopic:
    """Тесты для модели VKRTopic"""
    
    def test_valid_topic_creation(self):
        """Тест создания валидной темы"""
        topic = VKRTopic(
            title="Разработка системы рекомендаций",
            field="Информатика",
            level=EducationLevel.BACHELOR,
            description="Описание темы",
            keywords=["машинное обучение", "рекомендации"]
        )
        
        assert topic.title == "Разработка системы рекомендаций"
        assert topic.field == "Информатика"
        assert topic.level == EducationLevel.BACHELOR
        assert len(topic.keywords) == 2
        assert topic.status == TopicStatus.DRAFT  # Значение по умолчанию
    
    def test_invalid_topic_title_too_short(self):
        """Тест валидации слишком короткого названия"""
        with pytest.raises(ValidationError) as exc_info:
            VKRTopic(
                title="Коротко",  # Меньше 10 символов
                field="Информатика",
                level=EducationLevel.BACHELOR
            )
        
        assert "at least 10 characters" in str(exc_info.value)
    
    def test_invalid_topic_title_too_long(self):
        """Тест валидации слишком длинного названия"""
        long_title = "Очень длинное название темы " * 10  # Больше 200 символов
        
        with pytest.raises(ValidationError) as exc_info:
            VKRTopic(
                title=long_title,
                field="Информатика",
                level=EducationLevel.BACHELOR
            )
        
        assert "at most 200 characters" in str(exc_info.value)
    
    def test_relevance_score_validation(self):
        """Тест валидации оценки релевантности"""
        # Валидная оценка
        topic = VKRTopic(
            title="Тестовая тема",
            field="Информатика",
            level=EducationLevel.BACHELOR,
            relevance_score=0.8
        )
        assert topic.relevance_score == 0.8
        
        # Невалидная оценка (больше 1)
        with pytest.raises(ValidationError):
            VKRTopic(
                title="Тестовая тема",
                field="Информатика",
                level=EducationLevel.BACHELOR,
                relevance_score=1.5
            )
    
    def test_estimated_hours_validation(self):
        """Тест валидации оценочного времени"""
        # Валидное время
        topic = VKRTopic(
            title="Тестовая тема",
            field="Информатика",
            level=EducationLevel.BACHELOR,
            estimated_hours=120
        )
        assert topic.estimated_hours == 120
        
        # Невалидное время (меньше 1)
        with pytest.raises(ValidationError):
            VKRTopic(
                title="Тестовая тема",
                field="Информатика",
                level=EducationLevel.BACHELOR,
                estimated_hours=0
            )


class TestTopicRequest:
    """Тесты для модели TopicRequest"""
    
    def test_valid_request_creation(self):
        """Тест создания валидного запроса"""
        request = TopicRequest(
            field="Информатика",
            count=5,
            level=EducationLevel.BACHELOR
        )
        
        assert request.field == "Информатика"
        assert request.count == 5
        assert request.level == EducationLevel.BACHELOR
        assert request.include_trends is True  # Значение по умолчанию
        assert request.language == "ru"  # Значение по умолчанию
    
    def test_invalid_count_too_low(self):
        """Тест валидации слишком малого количества тем"""
        with pytest.raises(ValidationError):
            TopicRequest(
                field="Информатика",
                count=0  # Меньше 1
            )
    
    def test_invalid_count_too_high(self):
        """Тест валидации слишком большого количества тем"""
        with pytest.raises(ValidationError):
            TopicRequest(
                field="Информатика",
                count=25  # Больше 20
            )
    
    def test_min_relevance_score_validation(self):
        """Тест валидации минимальной оценки релевантности"""
        # Валидная оценка
        request = TopicRequest(
            field="Информатика",
            min_relevance_score=0.7
        )
        assert request.min_relevance_score == 0.7
        
        # Невалидная оценка
        with pytest.raises(ValidationError):
            TopicRequest(
                field="Информатика",
                min_relevance_score=1.5
            )


class TestTopicResponse:
    """Тесты для модели TopicResponse"""
    
    def test_valid_response_creation(self, sample_topics_list):
        """Тест создания валидного ответа"""
        topics = [VKRTopic(**topic_data) for topic_data in sample_topics_list]
        
        response = TopicResponse(
            topics=topics,
            total_count=len(topics),
            generation_time=1.5,
            model_used="openai:gpt-4.1"
        )
        
        assert len(response.topics) == 2
        assert response.total_count == 2
        assert response.generation_time == 1.5
        assert response.model_used == "openai:gpt-4.1"
    
    def test_quality_score_validation(self, sample_topics_list):
        """Тест валидации оценки качества"""
        topics = [VKRTopic(**topic_data) for topic_data in sample_topics_list]
        
        # Валидная оценка качества
        response = TopicResponse(
            topics=topics,
            total_count=len(topics),
            generation_time=1.0,
            model_used="test",
            quality_score=0.85
        )
        assert response.quality_score == 0.85
        
        # Невалидная оценка качества
        with pytest.raises(ValidationError):
            TopicResponse(
                topics=topics,
                total_count=len(topics),
                generation_time=1.0,
                model_used="test",
                quality_score=1.5  # Больше 1
            )
