"""
Тесты для агентов генерации тем
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.agents import VKRTopicAgent, TopicGenerationConfig
from src.models import EducationLevel, VKRTopic


class TestVKRTopicAgent:
    """Тесты для VKRTopicAgent"""
    
    @pytest.fixture
    def agent(self, mock_llm):
        """Создание агента с мок-моделью"""
        with patch('src.agents.vkr_topic_agent.ChatOpenAI') as mock_openai:
            mock_openai.return_value = mock_llm
            return VKRTopicAgent(model_name="openai:gpt-4.1")
    
    def test_agent_initialization(self, agent):
        """Тест инициализации агента"""
        assert agent.model_name == "openai:gpt-4.1"
        assert agent.llm is not None
        assert agent.prompt_template is not None
    
    def test_agent_initialization_anthropic(self, mock_llm):
        """Тест инициализации агента с Anthropic"""
        with patch('src.agents.vkr_topic_agent.ChatAnthropic') as mock_anthropic:
            mock_anthropic.return_value = mock_llm
            agent = VKRTopicAgent(model_name="anthropic:claude-sonnet-4")
            
            assert agent.model_name == "anthropic:claude-sonnet-4"
            mock_anthropic.assert_called_once()
    
    def test_agent_initialization_invalid_model(self):
        """Тест инициализации с невалидной моделью"""
        with pytest.raises(ValueError, match="Неподдерживаемая модель"):
            VKRTopicAgent(model_name="invalid:model")
    
    @pytest.mark.asyncio
    async def test_generate_topics_simple(self, agent, mock_llm):
        """Тест простой генерации тем"""
        # Настройка мока
        mock_response = MagicMock()
        mock_response.content = """
        1. Разработка системы рекомендаций на основе машинного обучения
        Актуальность: Машинное обучение активно развивается.
        Ключевые слова: машинное обучение, рекомендательные системы
        Методология: Разработка и тестирование алгоритмов
        Ожидаемые результаты: Функциональная система рекомендаций
        
        2. Анализ данных социальных сетей с использованием ИИ
        Актуальность: Социальные сети генерируют большие данные.
        Ключевые слова: анализ данных, социальные сети, ИИ
        Методология: Сбор и анализ данных
        Ожидаемые результаты: Инструменты для анализа
        """
        mock_llm.ainvoke.return_value = mock_response
        
        # Выполнение теста
        topics = await agent.generate_topics_simple(
            field="Информатика",
            count=2,
            level=EducationLevel.BACHELOR
        )
        
        # Проверки
        assert len(topics) == 2
        assert all(isinstance(topic, VKRTopic) for topic in topics)
        assert topics[0].field == "Информатика"
        assert topics[0].level == EducationLevel.BACHELOR
        assert "машинное обучение" in topics[0].keywords
        mock_llm.ainvoke.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_topics_with_config(self, agent, mock_llm):
        """Тест генерации тем с конфигурацией"""
        # Настройка мока
        mock_response = MagicMock()
        mock_response.content = """
        1. Исследование методов оптимизации нейронных сетей
        Актуальность: Нейронные сети требуют оптимизации.
        Ключевые слова: нейронные сети, оптимизация, глубокое обучение
        Методология: Экспериментальные исследования
        Ожидаемые результаты: Улучшенные алгоритмы оптимизации
        """
        mock_llm.ainvoke.return_value = mock_response
        
        # Создание конфигурации
        config = TopicGenerationConfig(
            field="Информатика",
            specialization="Машинное обучение",
            level=EducationLevel.MASTER,
            count=1,
            include_trends=True,
            include_methodology=True
        )
        
        # Выполнение теста
        topics = await agent.generate_topics(config)
        
        # Проверки
        assert len(topics) == 1
        assert topics[0].field == "Информатика"
        assert topics[0].specialization == "Машинное обучение"
        assert topics[0].level == EducationLevel.MASTER
        mock_llm.ainvoke.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_topics_error_handling(self, agent, mock_llm):
        """Тест обработки ошибок при генерации"""
        # Настройка мока для выброса исключения
        mock_llm.ainvoke.side_effect = Exception("API Error")
        
        # Выполнение теста
        with pytest.raises(Exception, match="API Error"):
            await agent.generate_topics_simple(
                field="Информатика",
                count=1
            )
    
    def test_parse_response_simple(self, agent):
        """Тест парсинга простого ответа"""
        response_text = """
        1. Разработка системы рекомендаций
        Актуальность: Система рекомендаций важна для пользователей.
        Ключевые слова: рекомендации, машинное обучение, алгоритмы
        Методология: Разработка и тестирование
        Ожидаемые результаты: Рабочая система рекомендаций
        """
        
        config = TopicGenerationConfig(
            field="Информатика",
            level=EducationLevel.BACHELOR,
            count=1
        )
        
        topics = agent._parse_response(response_text, config)
        
        assert len(topics) == 1
        assert topics[0].title == "Разработка системы рекомендаций"
        assert "рекомендации" in topics[0].keywords
        assert topics[0].field == "Информатика"
    
    def test_parse_response_multiple_topics(self, agent):
        """Тест парсинга ответа с несколькими темами"""
        response_text = """
        1. Первая тема
        Актуальность: Важность первой темы.
        Ключевые слова: тема1, важность
        Методология: Исследование
        Ожидаемые результаты: Результаты первой темы
        
        2. Вторая тема
        Актуальность: Важность второй темы.
        Ключевые слова: тема2, важность
        Методология: Анализ
        Ожидаемые результаты: Результаты второй темы
        """
        
        config = TopicGenerationConfig(
            field="Экономика",
            level=EducationLevel.MASTER,
            count=2
        )
        
        topics = agent._parse_response(response_text, config)
        
        assert len(topics) == 2
        assert topics[0].title == "Первая тема"
        assert topics[1].title == "Вторая тема"
        assert all(topic.field == "Экономика" for topic in topics)
        assert all(topic.level == EducationLevel.MASTER for topic in topics)


class TestTopicGenerationConfig:
    """Тесты для конфигурации генерации тем"""
    
    def test_valid_config_creation(self):
        """Тест создания валидной конфигурации"""
        config = TopicGenerationConfig(
            field="Информатика",
            specialization="Машинное обучение",
            level=EducationLevel.BACHELOR,
            count=5,
            include_trends=True,
            include_methodology=True,
            language="ru"
        )
        
        assert config.field == "Информатика"
        assert config.specialization == "Машинное обучение"
        assert config.level == EducationLevel.BACHELOR
        assert config.count == 5
        assert config.include_trends is True
        assert config.include_methodology is True
        assert config.language == "ru"
    
    def test_config_defaults(self):
        """Тест значений по умолчанию"""
        config = TopicGenerationConfig(field="Информатика")
        
        assert config.specialization is None
        assert config.level == EducationLevel.BACHELOR
        assert config.count == 5
        assert config.include_trends is True
        assert config.include_methodology is True
        assert config.language == "ru"
