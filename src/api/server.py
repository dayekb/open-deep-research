"""
FastAPI сервер для сервиса генерации тем ВКР
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import uuid
from typing import List, Optional
from loguru import logger

from ..agents import VKRTopicAgent, TopicGenerationConfig
from ..models import (
    TopicRequest, TopicResponse, TopicSearchRequest, TopicSearchResponse,
    TopicUpdateRequest, TopicStats, VKRTopic, EducationLevel, TopicStatus,
    StudentPreferences, DepartmentContext
)
from ..config import settings
from ..database import get_db, TopicRepository


# Создание FastAPI приложения
app = FastAPI(
    title="VKR Topic Generator API",
    description="API для генерации тем выпускных квалификационных работ",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Глобальный агент
topic_agent = None


@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    global topic_agent
    try:
        topic_agent = VKRTopicAgent()
        logger.info("VKR Topic Agent инициализирован")
    except Exception as e:
        logger.error(f"Ошибка инициализации агента: {e}")
        raise


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "VKR Topic Generator API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "model": settings.default_model
    }


@app.post("/generate-topics", response_model=TopicResponse)
async def generate_topics(
    request: TopicRequest,
    db: TopicRepository = Depends(get_db)
):
    """
    Генерация тем ВКР
    
    Args:
        request: Параметры генерации тем
        db: Репозиторий базы данных
        
    Returns:
        Сгенерированные темы
    """
    try:
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        logger.info(f"Запрос на генерацию тем: {request.field}, {request.count} тем")
        
        # Создание конфигурации
        config = TopicGenerationConfig(
            field=request.field,
            specialization=request.specialization,
            level=request.level,
            count=request.count,
            include_trends=request.include_trends,
            include_methodology=request.include_methodology,
            language=request.language,
            student_preferences=request.student_preferences,
            department_context=request.department_context,
            avoid_duplicates=request.avoid_duplicates
        )
        
        # Генерация тем
        topics = await topic_agent.generate_topics(config)
        
        # Сохранение в базу данных
        for topic in topics:
            topic.model_used = settings.default_model
            topic.generation_params = request.dict()
            await db.create_topic(topic)
        
        generation_time = time.time() - start_time
        
        # Вычисление оценки качества
        quality_score = sum(t.relevance_score or 0.5 for t in topics) / len(topics) if topics else 0
        
        response = TopicResponse(
            topics=topics,
            total_count=len(topics),
            generation_time=generation_time,
            model_used=settings.default_model,
            request_id=request_id,
            quality_score=quality_score
        )
        
        logger.info(f"Успешно сгенерировано {len(topics)} тем за {generation_time:.2f}с")
        return response
        
    except Exception as e:
        logger.error(f"Ошибка генерации тем: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/topics", response_model=TopicSearchResponse)
async def search_topics(
    query: str = Query(..., description="Поисковый запрос"),
    field: Optional[str] = Query(None, description="Фильтр по области"),
    level: Optional[EducationLevel] = Query(None, description="Фильтр по уровню"),
    status: Optional[TopicStatus] = Query(None, description="Фильтр по статусу"),
    limit: int = Query(20, ge=1, le=100, description="Количество результатов"),
    offset: int = Query(0, ge=0, description="Смещение"),
    db: TopicRepository = Depends(get_db)
):
    """
    Поиск тем ВКР
    
    Args:
        query: Поисковый запрос
        field: Фильтр по области знаний
        level: Фильтр по уровню образования
        status: Фильтр по статусу
        limit: Количество результатов
        offset: Смещение для пагинации
        db: Репозиторий базы данных
        
    Returns:
        Найденные темы
    """
    try:
        search_request = TopicSearchRequest(
            query=query,
            field=field,
            level=level,
            status=status,
            limit=limit,
            offset=offset
        )
        
        topics, total_count = await db.search_topics(search_request)
        
        response = TopicSearchResponse(
            topics=topics,
            total_count=total_count,
            page=offset // limit + 1,
            per_page=limit,
            has_next=offset + limit < total_count,
            has_prev=offset > 0
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Ошибка поиска тем: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/topics/{topic_id}", response_model=VKRTopic)
async def get_topic(
    topic_id: int,
    db: TopicRepository = Depends(get_db)
):
    """
    Получение темы по ID
    
    Args:
        topic_id: ID темы
        db: Репозиторий базы данных
        
    Returns:
        Тема ВКР
    """
    try:
        topic = await db.get_topic(topic_id)
        if not topic:
            raise HTTPException(status_code=404, detail="Тема не найдена")
        return topic
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения темы {topic_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/topics/{topic_id}", response_model=VKRTopic)
async def update_topic(
    topic_id: int,
    request: TopicUpdateRequest,
    db: TopicRepository = Depends(get_db)
):
    """
    Обновление темы
    
    Args:
        topic_id: ID темы
        request: Данные для обновления
        db: Репозиторий базы данных
        
    Returns:
        Обновленная тема
    """
    try:
        topic = await db.update_topic(topic_id, request)
        if not topic:
            raise HTTPException(status_code=404, detail="Тема не найдена")
        return topic
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления темы {topic_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/topics/{topic_id}")
async def delete_topic(
    topic_id: int,
    db: TopicRepository = Depends(get_db)
):
    """
    Удаление темы
    
    Args:
        topic_id: ID темы
        db: Репозиторий базы данных
        
    Returns:
        Результат удаления
    """
    try:
        success = await db.delete_topic(topic_id)
        if not success:
            raise HTTPException(status_code=404, detail="Тема не найдена")
        return {"message": "Тема успешно удалена"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления темы {topic_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", response_model=TopicStats)
async def get_stats(db: TopicRepository = Depends(get_db)):
    """
    Получение статистики по темам
    
    Args:
        db: Репозиторий базы данных
        
    Returns:
        Статистика по темам
    """
    try:
        stats = await db.get_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Ошибка получения статистики: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fields")
async def get_supported_fields():
    """
    Получение списка поддерживаемых областей знаний
    
    Returns:
        Список областей знаний
    """
    return {
        "fields": settings.supported_fields,
        "levels": settings.education_levels
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.server:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
