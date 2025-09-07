#!/usr/bin/env python3
"""
Прямой тест агента без API
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


async def test_agent_direct():
    """Прямой тест агента"""
    print("🤖 ПРЯМОЙ ТЕСТ АГЕНТА")
    print("=" * 40)
    
    # Проверяем API ключ
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"API ключ: {api_key[:20]}...")
    
    # Создаем агента
    try:
        agent = VKRTopicAgent()
        print("✅ Агент создан")
    except Exception as e:
        print(f"❌ Ошибка создания агента: {e}")
        return False
    
    # Тестируем генерацию
    print("\n📚 Генерация тем...")
    
    config = TopicGenerationConfig(
        field="Информатика",
        level=EducationLevel.BACHELOR,
        count=1
    )
    
    try:
        print("Отправляем запрос к модели...")
        topics = await agent.generate_topics(config)
        
        print(f"✅ Получено {len(topics)} тем")
        
        for i, topic in enumerate(topics, 1):
            print(f"\nТема {i}:")
            print(f"  Заголовок: {topic.title}")
            print(f"  Описание: {topic.description}")
            print(f"  Ключевые слова: {topic.keywords}")
            print(f"  Сложность: {topic.difficulty}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка генерации: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_raw_model():
    """Тест сырого вызова модели"""
    print("\n🔧 ТЕСТ СЫРОГО ВЫЗОВА МОДЕЛИ")
    print("=" * 40)
    
    from src.agents.vkr_topic_agent import VKRTopicAgent
    
    agent = VKRTopicAgent()
    
    # Тестируем прямое обращение к модели
    try:
        print("Тестируем прямое обращение к LLM...")
        
        # Создаем простой промпт
        prompt = "Привет! Ответь коротко: 'Тест прошел успешно'"
        
        # Вызываем модель напрямую
        response = await agent.llm.ainvoke(prompt)
        
        print(f"✅ Ответ модели: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Основная функция"""
    print("🧪 ПОЛНОЕ ТЕСТИРОВАНИЕ АГЕНТА")
    print("=" * 50)
    
    # Тест 1: Сырой вызов модели
    success1 = await test_raw_model()
    
    if success1:
        print("\n✅ Модель работает!")
        
        # Тест 2: Генерация тем
        success2 = await test_agent_direct()
        
        if success2:
            print("\n🎉 ВСЕ ТЕСТЫ ПРОШЛИ!")
        else:
            print("\n❌ Проблема с генерацией тем")
    else:
        print("\n❌ Проблема с моделью")


if __name__ == "__main__":
    asyncio.run(main())
