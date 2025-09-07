"""
Тесты для работы с базой данных
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock

from src.database.repository import TopicRepository
from src.database.models import TopicDB
from src.models import VKRTopic, TopicSearchRequest, EducationLevel, TopicStatus, TopicUpdateRequest


class TestTopicRepository:
    """Тесты для репозитория тем"""
    
    @pytest.mark.asyncio
    async def test_create_topic(self, topic_repository, sample_topic_data):
        """Тест создания темы"""
        topic = VKRTopic(**sample_topic_data)
        
        created_topic = await topic_repository.create_topic(topic)
        
        assert created_topic.id is not None
        assert created_topic.title == topic.title
        assert created_topic.field == topic.field
        assert created_topic.level == topic.level
        assert created_topic.status == TopicStatus.DRAFT
    
    @pytest.mark.asyncio
    async def test_get_topic_existing(self, topic_repository, sample_topic_data):
        """Тест получения существующей темы"""
        # Создаем тему
        topic = VKRTopic(**sample_topic_data)
        created_topic = await topic_repository.create_topic(topic)
        
        # Получаем тему
        retrieved_topic = await topic_repository.get_topic(created_topic.id)
        
        assert retrieved_topic is not None
        assert retrieved_topic.id == created_topic.id
        assert retrieved_topic.title == created_topic.title
    
    @pytest.mark.asyncio
    async def test_get_topic_not_found(self, topic_repository):
        """Тест получения несуществующей темы"""
        retrieved_topic = await topic_repository.get_topic(999)
        assert retrieved_topic is None
    
    @pytest.mark.asyncio
    async def test_update_topic_existing(self, topic_repository, sample_topic_data):
        """Тест обновления существующей темы"""
        # Создаем тему
        topic = VKRTopic(**sample_topic_data)
        created_topic = await topic_repository.create_topic(topic)
        
        # Обновляем тему
        update_data = TopicUpdateRequest(
            title="Обновленное название",
            description="Обновленное описание",
            status=TopicStatus.APPROVED
        )
        
        updated_topic = await topic_repository.update_topic(created_topic.id, update_data)
        
        assert updated_topic is not None
        assert updated_topic.title == "Обновленное название"
        assert updated_topic.description == "Обновленное описание"
        assert updated_topic.status == TopicStatus.APPROVED
    
    @pytest.mark.asyncio
    async def test_update_topic_not_found(self, topic_repository):
        """Тест обновления несуществующей темы"""
        update_data = TopicUpdateRequest(title="Новое название")
        updated_topic = await topic_repository.update_topic(999, update_data)
        assert updated_topic is None
    
    @pytest.mark.asyncio
    async def test_delete_topic_existing(self, topic_repository, sample_topic_data):
        """Тест удаления существующей темы"""
        # Создаем тему
        topic = VKRTopic(**sample_topic_data)
        created_topic = await topic_repository.create_topic(topic)
        
        # Удаляем тему
        result = await topic_repository.delete_topic(created_topic.id)
        
        assert result is True
        
        # Проверяем, что тема удалена
        deleted_topic = await topic_repository.get_topic(created_topic.id)
        assert deleted_topic is None
    
    @pytest.mark.asyncio
    async def test_delete_topic_not_found(self, topic_repository):
        """Тест удаления несуществующей темы"""
        result = await topic_repository.delete_topic(999)
        assert result is False
    
    @pytest.mark.asyncio
    async def test_search_topics_by_query(self, topic_repository, sample_topics_list):
        """Тест поиска тем по запросу"""
        # Создаем несколько тем
        for topic_data in sample_topics_list:
            topic = VKRTopic(**topic_data)
            await topic_repository.create_topic(topic)
        
        # Поиск по запросу
        search_request = TopicSearchRequest(
            query="машинное обучение",
            limit=10,
            offset=0
        )
        
        topics, total_count = await topic_repository.search_topics(search_request)
        
        assert total_count >= 0
        assert len(topics) <= 10
        # Проверяем, что найденные темы содержат ключевые слова поиска
        for topic in topics:
            search_terms = search_request.query.lower().split()
            topic_text = (topic.title + " " + (topic.description or "")).lower()
            assert any(term in topic_text for term in search_terms)
    
    @pytest.mark.asyncio
    async def test_search_topics_by_field(self, topic_repository, sample_topics_list):
        """Тест поиска тем по области"""
        # Создаем темы
        for topic_data in sample_topics_list:
            topic = VKRTopic(**topic_data)
            await topic_repository.create_topic(topic)
        
        # Поиск по области
        search_request = TopicSearchRequest(
            query="",
            field="Информатика",
            limit=10,
            offset=0
        )
        
        topics, total_count = await topic_repository.search_topics(search_request)
        
        assert total_count >= 0
        for topic in topics:
            assert topic.field == "Информатика"
    
    @pytest.mark.asyncio
    async def test_search_topics_by_level(self, topic_repository, sample_topics_list):
        """Тест поиска тем по уровню образования"""
        # Создаем темы
        for topic_data in sample_topics_list:
            topic = VKRTopic(**topic_data)
            await topic_repository.create_topic(topic)
        
        # Поиск по уровню
        search_request = TopicSearchRequest(
            query="",
            level=EducationLevel.BACHELOR,
            limit=10,
            offset=0
        )
        
        topics, total_count = await topic_repository.search_topics(search_request)
        
        assert total_count >= 0
        for topic in topics:
            assert topic.level == EducationLevel.BACHELOR
    
    @pytest.mark.asyncio
    async def test_search_topics_pagination(self, topic_repository):
        """Тест пагинации поиска тем"""
        # Создаем много тем для тестирования пагинации
        for i in range(15):
            topic = VKRTopic(
                title=f"Тема {i}",
                field="Информатика",
                level=EducationLevel.BACHELOR,
                description=f"Описание темы {i}"
            )
            await topic_repository.create_topic(topic)
        
        # Первая страница
        search_request = TopicSearchRequest(
            query="",
            limit=5,
            offset=0
        )
        topics_page1, total_count = await topic_repository.search_topics(search_request)
        
        # Вторая страница
        search_request.offset = 5
        topics_page2, _ = await topic_repository.search_topics(search_request)
        
        assert total_count == 15
        assert len(topics_page1) == 5
        assert len(topics_page2) == 5
        # Проверяем, что темы на разных страницах разные
        page1_ids = {topic.id for topic in topics_page1}
        page2_ids = {topic.id for topic in topics_page2}
        assert page1_ids.isdisjoint(page2_ids)
    
    @pytest.mark.asyncio
    async def test_get_stats(self, topic_repository, sample_topics_list):
        """Тест получения статистики"""
        # Создаем темы с разными характеристиками
        topics_data = [
            {"field": "Информатика", "level": EducationLevel.BACHELOR, "status": TopicStatus.DRAFT},
            {"field": "Информатика", "level": EducationLevel.MASTER, "status": TopicStatus.APPROVED},
            {"field": "Экономика", "level": EducationLevel.BACHELOR, "status": TopicStatus.DRAFT},
        ]
        
        for topic_data in topics_data:
            topic = VKRTopic(
                title=f"Тема {topic_data['field']}",
                field=topic_data["field"],
                level=topic_data["level"],
                status=topic_data["status"]
            )
            await topic_repository.create_topic(topic)
        
        # Получаем статистику
        stats = await topic_repository.get_stats()
        
        assert stats.total_topics == 3
        assert stats.by_field["Информатика"] == 2
        assert stats.by_field["Экономика"] == 1
        assert stats.by_level["Бакалавриат"] == 2
        assert stats.by_level["Магистратура"] == 1
        assert stats.by_status["DRAFT"] == 2
        assert stats.by_status["APPROVED"] == 1


class TestTopicDBModel:
    """Тесты для модели TopicDB"""
    
    def test_to_pydantic_conversion(self, sample_topic_data):
        """Тест конвертации в Pydantic модель"""
        # Создаем TopicDB
        topic_db = TopicDB(
            id=1,
            title=sample_topic_data["title"],
            field=sample_topic_data["field"],
            level=EducationLevel.BACHELOR,
            description=sample_topic_data["description"],
            keywords=sample_topic_data["keywords"],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Конвертируем в Pydantic
        pydantic_topic = topic_db.to_pydantic()
        
        assert isinstance(pydantic_topic, VKRTopic)
        assert pydantic_topic.id == 1
        assert pydantic_topic.title == sample_topic_data["title"]
        assert pydantic_topic.field == sample_topic_data["field"]
        assert pydantic_topic.level == EducationLevel.BACHELOR
        assert pydantic_topic.keywords == sample_topic_data["keywords"]
    
    def test_from_pydantic_creation(self, sample_topic_data):
        """Тест создания из Pydantic модели"""
        # Создаем Pydantic модель
        pydantic_topic = VKRTopic(**sample_topic_data)
        
        # Конвертируем в TopicDB
        topic_db = TopicDB.from_pydantic(pydantic_topic)
        
        assert isinstance(topic_db, TopicDB)
        assert topic_db.title == sample_topic_data["title"]
        assert topic_db.field == sample_topic_data["field"]
        assert topic_db.level == EducationLevel.BACHELOR
        assert topic_db.keywords == sample_topic_data["keywords"]
        assert topic_db.created_at is not None
        assert topic_db.updated_at is not None
