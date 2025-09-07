"""
SQLAlchemy модели для базы данных
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, Dict, Any

from ..models import EducationLevel, TopicStatus

Base = declarative_base()


class TopicDB(Base):
    """SQLAlchemy модель для хранения тем ВКР"""
    
    __tablename__ = "vkr_topics"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    field = Column(String(100), nullable=False, index=True)
    specialization = Column(String(100), nullable=True, index=True)
    level = Column(Enum(EducationLevel), nullable=False, index=True)
    
    description = Column(Text, nullable=True)
    keywords = Column(JSON, nullable=True)  # Список ключевых слов
    methodology = Column(Text, nullable=True)
    expected_results = Column(Text, nullable=True)
    
    relevance_score = Column(Float, nullable=True)
    difficulty_level = Column(String(50), nullable=True)
    estimated_hours = Column(Integer, nullable=True)
    
    status = Column(Enum(TopicStatus), nullable=False, default=TopicStatus.DRAFT, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Метаданные
    source = Column(String(50), nullable=False, default="ai_generated")
    model_used = Column(String(100), nullable=True)
    generation_params = Column(JSON, nullable=True)
    request_id = Column(String(100), nullable=True, index=True)
    
    def to_pydantic(self) -> 'VKRTopic':
        """Конвертация в Pydantic модель"""
        from ..models import VKRTopic
        
        return VKRTopic(
            id=self.id,
            title=self.title,
            field=self.field,
            specialization=self.specialization,
            level=self.level,
            description=self.description or "",
            keywords=self.keywords or [],
            methodology=self.methodology or "",
            expected_results=self.expected_results or "",
            relevance_score=self.relevance_score,
            difficulty_level=self.difficulty_level,
            estimated_hours=self.estimated_hours,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
            source=self.source,
            model_used=self.model_used,
            generation_params=self.generation_params
        )
    
    @classmethod
    def from_pydantic(cls, topic: 'VKRTopic') -> 'TopicDB':
        """Создание из Pydantic модели"""
        return cls(
            id=topic.id,
            title=topic.title,
            field=topic.field,
            specialization=topic.specialization,
            level=topic.level,
            description=topic.description,
            keywords=topic.keywords,
            methodology=topic.methodology,
            expected_results=topic.expected_results,
            relevance_score=topic.relevance_score,
            difficulty_level=topic.difficulty_level,
            estimated_hours=topic.estimated_hours,
            status=topic.status,
            created_at=topic.created_at or datetime.now(),
            updated_at=topic.updated_at or datetime.now(),
            source=topic.source,
            model_used=topic.model_used,
            generation_params=topic.generation_params,
            request_id=getattr(topic, 'request_id', None)
        )
