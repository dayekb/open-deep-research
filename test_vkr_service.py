#!/usr/bin/env python3
"""
Тест сервиса генерации тем ВКР с новым API ключом
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


async def test_vkr_service():
    """Тест сервиса генерации тем"""
    print("🚀 ТЕСТ СЕРВИСА ГЕНЕРАЦИИ ТЕМ ВКР")
    print("=" * 50)
    
    # Проверяем API ключ
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY не найден")
        return False
    
    print(f"✅ API ключ найден: {api_key[:20]}...")
    
    # Создаем агента
    try:
        agent = VKRTopicAgent()
        print("✅ Агент создан")
    except Exception as e:
        print(f"❌ Ошибка создания агента: {e}")
        return False
    
    # Тестируем генерацию тем
    print("\n📚 Генерация тем по информатике...")
    
    config = TopicGenerationConfig(
        field="Информатика",
        level=EducationLevel.BACHELOR,
        count=2
    )
    
    try:
        topics = await agent.generate_topics(config)
        print(f"✅ Сгенерировано {len(topics)} тем:")
        
        for i, topic in enumerate(topics, 1):
            print(f"\n{i}. {topic.title}")
            print(f"   Описание: {topic.description}")
            print(f"   Ключевые слова: {', '.join(topic.keywords)}")
            print(f"   Сложность: {topic.difficulty}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка генерации: {e}")
        return False


async def test_different_fields():
    """Тест разных направлений"""
    print("\n🔬 ТЕСТ РАЗНЫХ НАПРАВЛЕНИЙ")
    print("=" * 40)
    
    agent = VKRTopicAgent()
    
    test_configs = [
        ("Математика", EducationLevel.BACHELOR, 1),
        ("Физика", EducationLevel.MASTER, 1),
        ("Химия", EducationLevel.BACHELOR, 1)
    ]
    
    for field, level, count in test_configs:
        print(f"\n📖 {field} ({level.value})...")
        
        config = TopicGenerationConfig(
            field=field,
            level=level,
            count=count
        )
        
        try:
            topics = await agent.generate_topics(config)
            print(f"   ✅ {len(topics)} тем сгенерировано")
            if topics:
                print(f"   📝 Пример: {topics[0].title}")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")


async def main():
    """Основная функция"""
    print("🧪 ПОЛНОЕ ТЕСТИРОВАНИЕ СЕРВИСА ВКР")
    print("=" * 60)
    
    # Тест 1: Основная генерация
    success = await test_vkr_service()
    
    if success:
        print("\n🎉 Основной тест прошел успешно!")
        
        # Тест 2: Разные направления
        await test_different_fields()
        
        print("\n✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
        print("\n🚀 Сервис готов к использованию!")
        print("Запустите сервер: conda run python run_openrouter.py")
        
    else:
        print("\n❌ Тест не прошел")
        print("Проверьте настройки и API ключ")


if __name__ == "__main__":
    asyncio.run(main())
