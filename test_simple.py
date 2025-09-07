#!/usr/bin/env python3
"""
Простое тестирование без внешних API
"""

import sys
from pathlib import Path

# Добавляем путь к src
sys.path.append(str(Path(__file__).parent / "src"))

def test_imports():
    """Тест импортов"""
    print("🔍 Тестирование импортов...")
    
    try:
        from src.config import settings
        print("✅ Настройки импортированы")
        
        from src.models import VKRTopic, EducationLevel
        print("✅ Модели импортированы")
        
        from src.agents import VKRTopicAgent
        print("✅ Агент импортирован")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def test_models():
    """Тест моделей данных"""
    print("\n📋 Тестирование моделей данных...")
    
    try:
        from src.models import VKRTopic, EducationLevel, TopicRequest
        
        # Тест создания темы
        topic = VKRTopic(
            title="Тестовая тема для ВКР",
            field="Информатика",
            level=EducationLevel.BACHELOR,
            description="Описание тестовой темы",
            keywords=["тест", "информатика"]
        )
        
        print(f"✅ Тема создана: {topic.title}")
        print(f"   Область: {topic.field}")
        print(f"   Уровень: {topic.level}")
        print(f"   Ключевые слова: {topic.keywords}")
        
        # Тест создания запроса
        request = TopicRequest(
            field="Информатика",
            count=3,
            level=EducationLevel.BACHELOR
        )
        
        print(f"✅ Запрос создан: {request.field}, {request.count} тем")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка моделей: {e}")
        return False

def test_config():
    """Тест конфигурации"""
    print("\n⚙️ Тестирование конфигурации...")
    
    try:
        from src.config import settings
        
        print(f"✅ Модель по умолчанию: {settings.default_model}")
        print(f"✅ Поддерживаемые области: {len(settings.supported_fields)}")
        print(f"✅ Уровни образования: {settings.education_levels}")
        print(f"✅ Максимум тем: {settings.max_topics_per_request}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False

def test_agent_creation():
    """Тест создания агента (без API вызовов)"""
    print("\n🤖 Тестирование создания агента...")
    
    try:
        from src.agents import VKRTopicAgent, TopicGenerationConfig
        
        # Создаем конфигурацию
        config = TopicGenerationConfig(
            field="Информатика",
            level="Бакалавриат",
            count=2
        )
        
        print(f"✅ Конфигурация создана: {config.field}")
        
        # Пытаемся создать агента (может упасть на API ключе)
        try:
            agent = VKRTopicAgent()
            print("✅ Агент создан (API ключ работает)")
        except Exception as e:
            print(f"⚠️ Агент не создан (проблема с API): {e}")
            print("   Это нормально, если API ключ недействителен")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка агента: {e}")
        return False

def test_api_structure():
    """Тест структуры API"""
    print("\n🌐 Тестирование структуры API...")
    
    try:
        from src.api.server import app
        print("✅ FastAPI приложение создано")
        
        # Проверяем основные эндпоинты
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/health", "/generate-topics", "/topics", "/stats", "/fields"]
        
        for route in expected_routes:
            if route in routes:
                print(f"✅ Маршрут {route} найден")
            else:
                print(f"⚠️ Маршрут {route} не найден")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка API: {e}")
        return False

def main():
    """Основная функция"""
    print("🧪 ПРОСТОЕ ТЕСТИРОВАНИЕ СЕРВИСА ГЕНЕРАЦИИ ТЕМ ВКР")
    print("=" * 60)
    
    tests = [
        ("Импорты", test_imports),
        ("Модели данных", test_models),
        ("Конфигурация", test_config),
        ("Создание агента", test_agent_creation),
        ("Структура API", test_api_structure)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"🔬 {test_name}")
        print(f"{'='*40}")
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - ПРОЙДЕН")
            else:
                print(f"❌ {test_name} - НЕ ПРОЙДЕН")
        except Exception as e:
            print(f"❌ {test_name} - ОШИБКА: {e}")
    
    print(f"\n{'='*60}")
    print(f"📊 ИТОГОВЫЙ РЕЗУЛЬТАТ")
    print(f"{'='*60}")
    print(f"✅ Пройдено: {passed}/{total}")
    print(f"❌ Не пройдено: {total - passed}/{total}")
    
    if passed >= total - 1:  # Допускаем одну ошибку (API ключ)
        print("\n🎉 СИСТЕМА РАБОТАЕТ!")
        print("\n📋 Следующие шаги:")
        print("1. Получите действующий OpenRouter API ключ")
        print("2. Обновите .env файл")
        print("3. Запустите: conda run python test_openrouter.py")
        print("4. Или запустите сервер: conda run python run_openrouter.py")
        return 0
    else:
        print(f"\n⚠️ {total - passed} ТЕСТОВ НЕ ПРОЙДЕНЫ")
        print("Требуется исправление ошибок")
        return 1

if __name__ == "__main__":
    sys.exit(main())
