#!/usr/bin/env python3
"""
Отладочный тест агента
"""

import os
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Добавляем путь к src
sys.path.append(str(Path(__file__).parent / "src"))

# Принудительно загружаем .env
load_dotenv(override=True)

from src.agents import VKRTopicAgent, TopicGenerationConfig
from src.models import EducationLevel


async def test_agent_debug():
    """Отладочный тест агента"""
    print("🔍 ОТЛАДОЧНЫЙ ТЕСТ АГЕНТА")
    print("=" * 40)
    
    agent = VKRTopicAgent()
    
    # Тестируем генерацию
    config = TopicGenerationConfig(
        field="Информатика",
        level=EducationLevel.BACHELOR,
        count=1
    )
    
    print("Конфигурация:")
    print(f"  Поле: {config.field}")
    print(f"  Уровень: {config.level}")
    print(f"  Количество: {config.count}")
    
    try:
        print("\nГенерируем темы...")
        topics = await agent.generate_topics(config)
        
        print(f"\nРезультат: {len(topics)} тем")
        
        for i, topic in enumerate(topics, 1):
            print(f"\nТема {i}:")
            print(f"  Заголовок: {topic.title}")
            print(f"  Описание: {topic.description}")
            print(f"  Ключевые слова: {topic.keywords}")
            print(f"  Сложность: {topic.difficulty_level}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    asyncio.run(test_agent_debug())
