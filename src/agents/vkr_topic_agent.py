"""
Агент для генерации тем ВКР на основе Open Deep Research
"""

import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from loguru import logger

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from ..config import settings
from ..models.topic_models import VKRTopic, TopicRequest, TopicResponse, StudentPreferences, DepartmentContext


@dataclass
class TopicGenerationConfig:
    """Конфигурация для генерации тем"""
    field: str
    specialization: Optional[str] = None
    level: str = "Бакалавриат"
    count: int = 5
    include_trends: bool = True
    include_methodology: bool = True
    language: str = "ru"
    
    # Контекстная информация
    student_preferences: Optional[StudentPreferences] = None
    department_context: Optional[DepartmentContext] = None
    avoid_duplicates: bool = True


class VKRTopicAgent:
    """Агент для генерации тем ВКР"""
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Инициализация агента
        
        Args:
            model_name: Название модели для использования
        """
        self.model_name = model_name or settings.default_model
        self.llm = self._initialize_llm()
        self.prompt_template = self._create_prompt_template()
        
    def _initialize_llm(self):
        """Инициализация языковой модели"""
        if self.model_name.startswith("openai:"):
            model = self.model_name.split(":", 1)[1]
            return ChatOpenAI(
                model=model,
                api_key=settings.openai_api_key,
                temperature=0.7
            )
        elif self.model_name.startswith("anthropic:"):
            model = self.model_name.split(":", 1)[1]
            return ChatAnthropic(
                model=model,
                api_key=settings.anthropic_api_key,
                temperature=0.7
            )
        elif self.model_name.startswith("openrouter:"):
            model = self.model_name.split(":", 1)[1]
            return ChatOpenAI(
                model=model,
                api_key=settings.openrouter_api_key,
                base_url="https://openrouter.ai/api/v1",
                temperature=0.7
            )
        else:
            raise ValueError(f"Неподдерживаемая модель: {self.model_name}")
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """Создание шаблона промпта для генерации тем"""
        return ChatPromptTemplate.from_messages([
            SystemMessage(content="""Ты - эксперт по академическому планированию и генерации тем для выпускных квалификационных работ (ВКР).

Твоя задача - генерировать актуальные, научно обоснованные и практически значимые темы ВКР для различных областей знаний.

При генерации тем учитывай:
1. Актуальность и востребованность темы в современной науке и практике
2. Возможность проведения исследования в рамках учебного процесса
3. Наличие достаточной научной базы для исследования
4. Практическую значимость результатов
5. Соответствие уровню образования (бакалавриат/магистратура/аспирантура)

Формат ответа (обязательно JSON):
```json
{
  "topics": [
    {
      "title": "Название темы",
      "description": "Краткое описание актуальности",
      "keywords": ["ключевое", "слово1", "слово2"],
      "methodology": "Предполагаемые методы исследования",
      "expected_results": "Ожидаемые результаты",
      "difficulty": "Легкая/Средняя/Сложная"
    }
  ]
}
```

Генерируй темы на русском языке, если не указано иное. ОБЯЗАТЕЛЬНО возвращай только валидный JSON без дополнительного текста."""),
            HumanMessage(content="""Сгенерируй {count} тем ВКР по направлению "{field}" 
            {specialization_text} для уровня "{level}".
            
            {trends_text}
            {methodology_text}
            {student_context_text}
            {department_context_text}
            {duplicate_avoidance_text}
            
            Убедись, что темы:
            - Актуальны и современны
            - Соответствуют уровню образования
            - Имеют практическую значимость
            - Могут быть исследованы в рамках учебного процесса
            {personalization_text}""")
        ])
    
    async def generate_topics(self, config: TopicGenerationConfig) -> List[VKRTopic]:
        """
        Генерация тем ВКР
        
        Args:
            config: Конфигурация генерации
            
        Returns:
            Список сгенерированных тем
        """
        try:
            logger.info(f"Генерация {config.count} тем для {config.field}")
            
            # Подготовка параметров промпта
            specialization_text = f"специализация: {config.specialization}" if config.specialization else ""
            trends_text = "Включи анализ современных трендов и направлений развития." if config.include_trends else ""
            methodology_text = "Включи описание методологии исследования." if config.include_methodology else ""
            
            # Контекстная информация
            student_context_text = self._format_student_context(config.student_preferences) if hasattr(config, 'student_preferences') and config.student_preferences else ""
            department_context_text = self._format_department_context(config.department_context) if hasattr(config, 'department_context') and config.department_context else ""
            duplicate_avoidance_text = self._format_duplicate_avoidance(config.avoid_duplicates, config.department_context) if hasattr(config, 'avoid_duplicates') and config.avoid_duplicates else ""
            personalization_text = self._format_personalization(config.student_preferences) if hasattr(config, 'student_preferences') and config.student_preferences else ""
            
            # Формирование промпта
            prompt = self.prompt_template.format_messages(
                count=config.count,
                field=config.field,
                specialization_text=specialization_text,
                level=config.level,
                trends_text=trends_text,
                methodology_text=methodology_text,
                student_context_text=student_context_text,
                department_context_text=department_context_text,
                duplicate_avoidance_text=duplicate_avoidance_text,
                personalization_text=personalization_text
            )
            
            # Генерация ответа
            response = await self.llm.ainvoke(prompt)
            
            # Парсинг ответа
            logger.info(f"Ответ модели: {response.content[:200]}...")
            topics = self._parse_response(response.content, config)
            
            logger.info(f"Успешно сгенерировано {len(topics)} тем")
            return topics
            
        except Exception as e:
            logger.error(f"Ошибка при генерации тем: {e}")
            raise
    
    def _parse_response(self, response: str, config: TopicGenerationConfig) -> List[VKRTopic]:
        """Парсинг ответа модели в структурированные темы"""
        topics = []
        
        try:
            # Сначала пробуем парсить JSON
            import json
            
            # Ищем JSON в ответе
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                
                # Парсим темы из JSON
                for topic_data in data.get('topics', []):
                    topic = VKRTopic(
                        title=topic_data.get('title', ''),
                        field=config.field,
                        specialization=config.specialization,
                        level=config.level,
                        description=topic_data.get('description', ''),
                        keywords=topic_data.get('keywords', []),
                        methodology=topic_data.get('methodology', ''),
                        expected_results=topic_data.get('expected_results', ''),
                        difficulty_level=topic_data.get('difficulty', 'Средняя')
                    )
                    topics.append(topic)
                
                return topics[:config.count]
        
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.warning(f"Ошибка парсинга JSON: {e}, пробуем текстовый парсинг")
        
        # Fallback: простой парсинг по номерам тем
        lines = response.split('\n')
        current_topic = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Проверка на начало новой темы (номер + название)
            if line[0].isdigit() and '.' in line:
                if current_topic:
                    topics.append(current_topic)
                
                # Извлечение названия темы
                title = line.split('.', 1)[1].strip()
                current_topic = VKRTopic(
                    title=title,
                    field=config.field,
                    specialization=config.specialization,
                    level=config.level,
                    description="",
                    keywords=[],
                    methodology="",
                    expected_results=""
                )
            elif current_topic:
                # Добавление дополнительной информации к текущей теме
                if "актуальность" in line.lower() or "описание" in line.lower():
                    current_topic.description = line
                elif "ключевые слова" in line.lower() or "keywords" in line.lower():
                    # Извлечение ключевых слов
                    keywords_text = line.split(':', 1)[1] if ':' in line else line
                    current_topic.keywords = [kw.strip() for kw in keywords_text.split(',')]
                elif "метод" in line.lower():
                    current_topic.methodology = line
                elif "результат" in line.lower():
                    current_topic.expected_results = line
        
        # Добавление последней темы
        if current_topic:
            topics.append(current_topic)
        
        return topics[:config.count]
    
    def _format_student_context(self, preferences) -> str:
        """Форматирование контекста студента"""
        if not preferences:
            return ""
        
        context_parts = []
        
        if preferences.interests:
            context_parts.append(f"Области интересов студента: {', '.join(preferences.interests)}")
        
        if preferences.skills:
            context_parts.append(f"Навыки студента: {', '.join(preferences.skills)}")
        
        if preferences.career_goals:
            context_parts.append(f"Карьерные цели: {', '.join(preferences.career_goals)}")
        
        if preferences.preferred_technologies:
            context_parts.append(f"Предпочитаемые технологии: {', '.join(preferences.preferred_technologies)}")
        
        if preferences.work_style:
            context_parts.append(f"Стиль работы: {preferences.work_style}")
        
        if preferences.complexity_preference:
            context_parts.append(f"Предпочтение сложности: {preferences.complexity_preference}")
        
        return "\n".join(context_parts) if context_parts else ""
    
    def _format_department_context(self, context) -> str:
        """Форматирование контекста кафедры"""
        if not context:
            return ""
        
        context_parts = []
        
        if context.research_directions:
            context_parts.append(f"Направления исследований кафедры: {', '.join(context.research_directions)}")
        
        if context.available_resources:
            context_parts.append(f"Доступные ресурсы: {', '.join(context.available_resources)}")
        
        if context.supervisor_expertise:
            context_parts.append(f"Экспертиза научных руководителей: {', '.join(context.supervisor_expertise)}")
        
        if context.recent_publications:
            context_parts.append(f"Недавние публикации: {', '.join(context.recent_publications[:3])}")  # Ограничиваем количество
        
        return "\n".join(context_parts) if context_parts else ""
    
    def _format_duplicate_avoidance(self, avoid_duplicates: bool, department_context) -> str:
        """Форматирование инструкций по избежанию дублирования"""
        if not avoid_duplicates or not department_context or not department_context.existing_topics:
            return ""
        
        existing_topics_text = "\n".join([f"- {topic}" for topic in department_context.existing_topics[:10]])  # Ограничиваем количество
        return f"""
ВАЖНО: Избегай дублирования с существующими темами на кафедре:
{existing_topics_text}

Генерируй только новые, уникальные темы, которые не пересекаются с перечисленными выше."""
    
    def _format_personalization(self, preferences) -> str:
        """Форматирование персонализации"""
        if not preferences:
            return ""
        
        personalization_parts = []
        
        if preferences.interests:
            personalization_parts.append("учитывай интересы студента")
        
        if preferences.skills:
            personalization_parts.append("соответствуй навыкам студента")
        
        if preferences.career_goals:
            personalization_parts.append("способствуй достижению карьерных целей")
        
        if personalization_parts:
            return f"Персонализируй темы, чтобы они {', '.join(personalization_parts)}."
        
        return ""
    
    async def generate_topics_simple(self, field: str, count: int = 5, 
                                   specialization: Optional[str] = None,
                                   level: str = "Бакалавриат") -> List[VKRTopic]:
        """
        Упрощенный метод генерации тем
        
        Args:
            field: Область знаний
            count: Количество тем
            specialization: Специализация
            level: Уровень образования
            
        Returns:
            Список тем
        """
        config = TopicGenerationConfig(
            field=field,
            specialization=specialization,
            level=level,
            count=count
        )
        return await self.generate_topics(config)
