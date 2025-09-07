"""
Базовые примеры использования сервиса генерации тем ВКР
"""

import asyncio
import sys
import os

# Добавляем путь к src в sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.agents import VKRTopicAgent, TopicGenerationConfig
from src.models import EducationLevel


async def basic_generation_example():
    """Базовый пример генерации тем"""
    print("=== Базовый пример генерации тем ВКР ===\n")
    
    # Инициализация агента
    agent = VKRTopicAgent()
    
    # Генерация тем для информатики
    print("Генерация тем по направлению 'Информатика':")
    topics = await agent.generate_topics_simple(
        field="Информатика",
        count=3,
        level=EducationLevel.BACHELOR
    )
    
    for i, topic in enumerate(topics, 1):
        print(f"\n{i}. {topic.title}")
        print(f"   Описание: {topic.description}")
        print(f"   Ключевые слова: {', '.join(topic.keywords)}")
        print(f"   Методология: {topic.methodology}")
        print(f"   Ожидаемые результаты: {topic.expected_results}")


async def specialized_generation_example():
    """Пример генерации тем с указанием специализации"""
    print("\n=== Генерация тем с специализацией ===\n")
    
    agent = VKRTopicAgent()
    
    # Конфигурация для машинного обучения
    config = TopicGenerationConfig(
        field="Информатика",
        specialization="Машинное обучение и искусственный интеллект",
        level=EducationLevel.MASTER,
        count=2,
        include_trends=True,
        include_methodology=True
    )
    
    topics = await agent.generate_topics(config)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n{i}. {topic.title}")
        print(f"   Уровень: {topic.level}")
        print(f"   Специализация: {topic.specialization}")
        print(f"   Описание: {topic.description}")


async def different_fields_example():
    """Пример генерации тем для разных областей"""
    print("\n=== Генерация тем для разных областей ===\n")
    
    agent = VKRTopicAgent()
    
    fields = ["Экономика", "Психология", "Медицина"]
    
    for field in fields:
        print(f"\n--- {field} ---")
        topics = await agent.generate_topics_simple(
            field=field,
            count=2,
            level=EducationLevel.BACHELOR
        )
        
        for topic in topics:
            print(f"• {topic.title}")


async def main():
    """Основная функция с примерами"""
    try:
        await basic_generation_example()
        await specialized_generation_example()
        await different_fields_example()
        
        print("\n=== Все примеры выполнены успешно! ===")
        
    except Exception as e:
        print(f"Ошибка при выполнении примеров: {e}")
        print("Убедитесь, что настроены API ключи в файле .env")


if __name__ == "__main__":
    asyncio.run(main())
