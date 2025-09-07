"""
Конфигурация сервиса генерации тем ВКР
"""

from pydantic_settings import BaseSettings
from typing import Optional, List
from enum import Enum


class ModelProvider(str, Enum):
    """Провайдеры языковых моделей"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    OPENROUTER = "openrouter"


class SearchProvider(str, Enum):
    """Провайдеры поиска"""
    TAVILY = "tavily"
    GOOGLE = "google"
    BING = "bing"


class Settings(BaseSettings):
    """Основные настройки приложения"""
    
    # API ключи
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    langchain_api_key: Optional[str] = None
    
    # Настройки трассировки
    langchain_tracing_v2: bool = False
    langchain_project: str = "vkr-topic-generator"
    
    # База данных
    database_url: str = "sqlite:///./vkr_topics.db"
    
    # Сервер
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Модели по умолчанию
    default_model: str = "openrouter:deepseek/deepseek-chat-v3.1:free"
    default_search_api: str = "tavily"
    
    # Ограничения
    max_topics_per_request: int = 10
    default_topics_count: int = 5
    
    # Настройки генерации
    min_topic_length: int = 50
    max_topic_length: int = 200
    require_relevance_score: bool = True
    min_relevance_score: float = 0.7
    
    # Поддерживаемые области знаний
    supported_fields: List[str] = [
        "Информатика",
        "Математика", 
        "Физика",
        "Химия",
        "Биология",
        "Экономика",
        "Менеджмент",
        "Право",
        "Психология",
        "Педагогика",
        "Медицина",
        "Инженерия"
    ]
    
    # Уровни образования
    education_levels: List[str] = [
        "Бакалавриат",
        "Магистратура", 
        "Аспирантура",
        "Специалитет"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Глобальный экземпляр настроек
settings = Settings()
