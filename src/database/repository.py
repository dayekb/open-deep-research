"""
Репозиторий для работы с темами ВКР
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import List, Tuple, Optional, Dict, Any
from loguru import logger

from .models import TopicDB
from ..models import (
    VKRTopic, TopicSearchRequest, TopicUpdateRequest, 
    TopicStats, EducationLevel, TopicStatus
)


class TopicRepository:
    """Репозиторий для работы с темами ВКР"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_topic(self, topic: VKRTopic) -> VKRTopic:
        """Создание новой темы"""
        try:
            db_topic = TopicDB.from_pydantic(topic)
            self.db.add(db_topic)
            self.db.commit()
            self.db.refresh(db_topic)
            
            logger.info(f"Создана тема: {db_topic.title}")
            return db_topic.to_pydantic()
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Ошибка создания темы: {e}")
            raise
    
    async def get_topic(self, topic_id: int) -> Optional[VKRTopic]:
        """Получение темы по ID"""
        try:
            db_topic = self.db.query(TopicDB).filter(TopicDB.id == topic_id).first()
            return db_topic.to_pydantic() if db_topic else None
            
        except Exception as e:
            logger.error(f"Ошибка получения темы {topic_id}: {e}")
            raise
    
    async def update_topic(self, topic_id: int, update_data: TopicUpdateRequest) -> Optional[VKRTopic]:
        """Обновление темы"""
        try:
            db_topic = self.db.query(TopicDB).filter(TopicDB.id == topic_id).first()
            if not db_topic:
                return None
            
            # Обновление полей
            update_dict = update_data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(db_topic, field, value)
            
            self.db.commit()
            self.db.refresh(db_topic)
            
            logger.info(f"Обновлена тема {topic_id}")
            return db_topic.to_pydantic()
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Ошибка обновления темы {topic_id}: {e}")
            raise
    
    async def delete_topic(self, topic_id: int) -> bool:
        """Удаление темы"""
        try:
            db_topic = self.db.query(TopicDB).filter(TopicDB.id == topic_id).first()
            if not db_topic:
                return False
            
            self.db.delete(db_topic)
            self.db.commit()
            
            logger.info(f"Удалена тема {topic_id}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Ошибка удаления темы {topic_id}: {e}")
            raise
    
    async def search_topics(self, search_request: TopicSearchRequest) -> Tuple[List[VKRTopic], int]:
        """Поиск тем по запросу"""
        try:
            query = self.db.query(TopicDB)
            
            # Поиск по тексту
            if search_request.query:
                search_term = f"%{search_request.query}%"
                query = query.filter(
                    or_(
                        TopicDB.title.ilike(search_term),
                        TopicDB.description.ilike(search_term),
                        TopicDB.methodology.ilike(search_term)
                    )
                )
            
            # Фильтры
            if search_request.field:
                query = query.filter(TopicDB.field == search_request.field)
            
            if search_request.level:
                query = query.filter(TopicDB.level == search_request.level)
            
            if search_request.status:
                query = query.filter(TopicDB.status == search_request.status)
            
            # Подсчет общего количества
            total_count = query.count()
            
            # Пагинация
            topics = query.offset(search_request.offset).limit(search_request.limit).all()
            
            # Конвертация в Pydantic модели
            pydantic_topics = [topic.to_pydantic() for topic in topics]
            
            logger.info(f"Найдено {len(pydantic_topics)} тем из {total_count}")
            return pydantic_topics, total_count
            
        except Exception as e:
            logger.error(f"Ошибка поиска тем: {e}")
            raise
    
    async def get_stats(self) -> TopicStats:
        """Получение статистики по темам"""
        try:
            # Общее количество тем
            total_topics = self.db.query(TopicDB).count()
            
            # По областям знаний
            by_field = {}
            field_stats = self.db.query(
                TopicDB.field, 
                func.count(TopicDB.id).label('count')
            ).group_by(TopicDB.field).all()
            
            for field, count in field_stats:
                by_field[field] = count
            
            # По уровням образования
            by_level = {}
            level_stats = self.db.query(
                TopicDB.level,
                func.count(TopicDB.id).label('count')
            ).group_by(TopicDB.level).all()
            
            for level, count in level_stats:
                by_level[level] = count
            
            # По статусам
            by_status = {}
            status_stats = self.db.query(
                TopicDB.status,
                func.count(TopicDB.id).label('count')
            ).group_by(TopicDB.status).all()
            
            for status, count in status_stats:
                by_status[status] = count
            
            # Средняя оценка релевантности
            avg_relevance = self.db.query(
                func.avg(TopicDB.relevance_score)
            ).filter(TopicDB.relevance_score.isnot(None)).scalar()
            
            # Популярные ключевые слова
            # Это упрощенная версия - в реальности нужен более сложный анализ
            popular_keywords = []
            
            stats = TopicStats(
                total_topics=total_topics,
                by_field=by_field,
                by_level=by_level,
                by_status=by_status,
                avg_relevance_score=float(avg_relevance) if avg_relevance else None,
                most_popular_keywords=popular_keywords
            )
            
            logger.info(f"Получена статистика: {total_topics} тем")
            return stats
            
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            raise


# Зависимость для получения репозитория
def get_db() -> TopicRepository:
    """Получение экземпляра репозитория"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from ..config import settings
    
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    try:
        return TopicRepository(db)
    finally:
        db.close()
