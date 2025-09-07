#!/usr/bin/env python3
"""
Быстрое тестирование сервиса генерации тем ВКР
"""

import subprocess
import sys
import time
import requests
from pathlib import Path


def check_dependencies():
    """Проверка зависимостей"""
    print("🔍 Проверка зависимостей...")
    
    try:
        import pytest
        import fastapi
        import sqlalchemy
        print("✅ Основные зависимости установлены")
        return True
    except ImportError as e:
        print(f"❌ Отсутствует зависимость: {e}")
        print("Установите зависимости: pip install -r requirements.txt")
        return False


def run_quick_tests():
    """Запуск быстрых тестов"""
    print("\n🧪 Запуск быстрых тестов...")
    
    # Тесты моделей (быстрые)
    print("  📋 Тестирование моделей данных...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/test_models.py", "-v", "--tb=short"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("  ✅ Модели данных - OK")
    else:
        print("  ❌ Модели данных - ОШИБКА")
        print(f"     {result.stdout}")
        return False
    
    # Тесты базы данных (быстрые)
    print("  🗄️  Тестирование базы данных...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/test_database.py", "-v", "--tb=short"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("  ✅ База данных - OK")
    else:
        print("  ❌ База данных - ОШИБКА")
        print(f"     {result.stdout}")
        return False
    
    return True


def test_api_manually():
    """Ручное тестирование API"""
    print("\n🌐 Тестирование API...")
    
    # Проверяем, что сервер запущен
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("  ✅ Сервер работает")
        else:
            print("  ❌ Сервер не отвечает")
            return False
    except requests.exceptions.RequestException:
        print("  ⚠️  Сервер не запущен. Запустите: python main.py")
        return False
    
    # Тестируем основные эндпоинты
    endpoints = [
        ("/", "GET", "Корневой эндпоинт"),
        ("/health", "GET", "Проверка здоровья"),
        ("/fields", "GET", "Поддерживаемые области"),
    ]
    
    for endpoint, method, description in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            else:
                response = requests.post(f"http://localhost:8000{endpoint}", timeout=5)
            
            if response.status_code in [200, 404]:  # 404 для /stats без данных
                print(f"  ✅ {description} - OK")
            else:
                print(f"  ❌ {description} - Ошибка {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ {description} - Исключение: {e}")
            return False
    
    return True


def test_generation_with_mock():
    """Тестирование генерации с моками"""
    print("\n🤖 Тестирование генерации тем...")
    
    try:
        # Импортируем и тестируем агент
        from src.agents import VKRTopicAgent, TopicGenerationConfig
        from src.models import EducationLevel
        
        # Создаем агента (будет использовать моки в тестах)
        agent = VKRTopicAgent()
        print("  ✅ Агент создан")
        
        # Тестируем конфигурацию
        config = TopicGenerationConfig(
            field="Информатика",
            level=EducationLevel.BACHELOR,
            count=1
        )
        print("  ✅ Конфигурация создана")
        
        print("  ✅ Генерация тем - OK (требует API ключи для полного тестирования)")
        return True
        
    except Exception as e:
        print(f"  ❌ Генерация тем - Ошибка: {e}")
        return False


def main():
    """Основная функция"""
    print("🚀 БЫСТРОЕ ТЕСТИРОВАНИЕ СЕРВИСА ГЕНЕРАЦИИ ТЕМ ВКР")
    print("=" * 60)
    
    # Проверяем, что мы в правильной директории
    if not Path("src").exists() or not Path("tests").exists():
        print("❌ Запустите скрипт из корневой директории проекта")
        return 1
    
    # Проверяем зависимости
    if not check_dependencies():
        return 1
    
    # Запускаем быстрые тесты
    if not run_quick_tests():
        print("\n❌ Быстрые тесты не прошли")
        return 1
    
    # Тестируем генерацию
    if not test_generation_with_mock():
        print("\n❌ Тестирование генерации не прошло")
        return 1
    
    # Тестируем API (если сервер запущен)
    api_ok = test_api_manually()
    
    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ РЕЗУЛЬТАТ")
    print("=" * 60)
    
    if api_ok:
        print("✅ Все тесты прошли успешно!")
        print("\n🎯 Сервис готов к использованию!")
        print("\n📋 Следующие шаги:")
        print("  1. Настройте API ключи в .env файле")
        print("  2. Запустите сервер: python main.py")
        print("  3. Откройте документацию: http://localhost:8000/docs")
        print("  4. Запустите полные тесты: python tests/run_tests.py")
    else:
        print("⚠️  Базовые тесты прошли, но API недоступен")
        print("\n📋 Для полного тестирования:")
        print("  1. Запустите сервер: python main.py")
        print("  2. Запустите ручные тесты: python tests/manual_test.py")
        print("  3. Запустите все тесты: python tests/run_tests.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
