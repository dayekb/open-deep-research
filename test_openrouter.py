#!/usr/bin/env python3
"""
Быстрое тестирование с OpenRouter API
"""

import os
import asyncio
import sys
from pathlib import Path

# Добавляем путь к src
sys.path.append(str(Path(__file__).parent / "src"))

from src.agents import VKRTopicAgent, TopicGenerationConfig
from src.models import EducationLevel


async def test_openrouter_generation():
    """Тест генерации тем с OpenRouter"""
    print("🤖 Тестирование генерации тем с OpenRouter")
    print("=" * 50)
    
    # Проверяем API ключ
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY не найден в переменных окружения")
        print("Установите ключ: export OPENROUTER_API_KEY=your_key_here")
        return False
    
    print(f"✅ API ключ найден: {api_key[:10]}...")
    
    try:
        # Создаем агента с OpenRouter
        agent = VKRTopicAgent(model_name="openrouter:meta-llama/llama-3.1-8b-instruct:free")
        print("✅ Агент создан")
        
        # Тестируем простую генерацию
        print("\n📚 Генерация тем по информатике...")
        topics = await agent.generate_topics_simple(
            field="Информатика",
            count=2,
            level=EducationLevel.BACHELOR
        )
        
        print(f"✅ Сгенерировано {len(topics)} тем")
        
        # Выводим результаты
        for i, topic in enumerate(topics, 1):
            print(f"\n{i}. {topic.title}")
            print(f"   Область: {topic.field}")
            print(f"   Уровень: {topic.level}")
            if topic.description:
                print(f"   Описание: {topic.description[:100]}...")
            if topic.keywords:
                print(f"   Ключевые слова: {', '.join(topic.keywords)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


async def test_different_fields():
    """Тест генерации для разных областей"""
    print("\n🔬 Тестирование разных областей знаний")
    print("=" * 50)
    
    agent = VKRTopicAgent()
    fields = ["Экономика", "Медицина", "Психология"]
    
    for field in fields:
        try:
            print(f"\n📖 {field}:")
            topics = await agent.generate_topics_simple(
                field=field,
                count=1,
                level=EducationLevel.BACHELOR
            )
            
            if topics:
                print(f"  ✅ {topics[0].title}")
            else:
                print(f"  ❌ Не удалось сгенерировать тему")
                
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")


async def test_api_server():
    """Тест API сервера"""
    print("\n🌐 Тестирование API сервера")
    print("=" * 50)
    
    try:
        import requests
        
        # Проверяем, что сервер запущен
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Сервер работает")
            
            # Тестируем генерацию через API
            request_data = {
                "field": "Информатика",
                "count": 1,
                "level": "Бакалавриат"
            }
            
            response = requests.post(
                "http://localhost:8000/generate-topics",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API генерация работает: {data['total_count']} тем")
                if data['topics']:
                    print(f"   Пример: {data['topics'][0]['title']}")
            else:
                print(f"❌ Ошибка API: {response.status_code}")
                print(f"   Ответ: {response.text}")
                
        else:
            print("❌ Сервер не отвечает")
            print("Запустите сервер: python main.py")
            
    except ImportError:
        print("❌ requests не установлен: pip install requests")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def main():
    """Основная функция"""
    print("🚀 ТЕСТИРОВАНИЕ С OPENROUTER API")
    print("=" * 60)
    
    # Проверяем, что мы в правильной директории
    if not Path("src").exists():
        print("❌ Запустите скрипт из корневой директории проекта")
        return 1
    
    # Запускаем тесты
    success = asyncio.run(test_openrouter_generation())
    
    if success:
        print("\n🎉 Базовое тестирование прошло успешно!")
        
        # Дополнительные тесты
        asyncio.run(test_different_fields())
        asyncio.run(test_api_server())
        
        print("\n📋 Следующие шаги:")
        print("1. Запустите сервер: python main.py")
        print("2. Откройте документацию: http://localhost:8000/docs")
        print("3. Запустите полные тесты: make test")
        
        return 0
    else:
        print("\n❌ Тестирование не прошло")
        print("Проверьте API ключ и настройки")
        return 1


if __name__ == "__main__":
    sys.exit(main())
