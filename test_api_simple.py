#!/usr/bin/env python3
"""
Простое тестирование API
"""

import requests
import json

def test_api():
    """Тестирование API"""
    base_url = "http://localhost:8000"
    
    print("🌐 Тестирование API сервиса генерации тем ВКР")
    print("=" * 50)
    
    # Тест 1: Проверка здоровья
    print("\n1. Проверка здоровья сервиса...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Сервис работает: {data['status']}")
            print(f"   Модель: {data.get('model', 'N/A')}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False
    
    # Тест 2: Получение поддерживаемых областей
    print("\n2. Получение поддерживаемых областей...")
    try:
        response = requests.get(f"{base_url}/fields")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Области знаний: {', '.join(data['fields'][:5])}...")
            print(f"   Уровни образования: {', '.join(data['levels'])}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 3: Генерация тем (может не работать из-за API ключа)
    print("\n3. Тестирование генерации тем...")
    try:
        request_data = {
            "field": "Информатика",
            "count": 2,
            "level": "Бакалавриат"
        }
        
        response = requests.post(f"{base_url}/generate-topics", json=request_data)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Успешно сгенерировано {data['total_count']} тем")
            print(f"   Время генерации: {data['generation_time']:.2f}с")
            print(f"   Модель: {data['model_used']}")
            
            # Выводим темы
            for i, topic in enumerate(data['topics'], 1):
                print(f"\n   {i}. {topic['title']}")
                if topic.get('description'):
                    print(f"      Описание: {topic['description'][:100]}...")
                if topic.get('keywords'):
                    print(f"      Ключевые слова: {', '.join(topic['keywords'])}")
        else:
            print(f"❌ Ошибка генерации: {response.status_code}")
            print(f"   Ответ: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 4: Статистика
    print("\n4. Получение статистики...")
    try:
        response = requests.get(f"{base_url}/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Статистика получена")
            print(f"   Всего тем: {data['total_topics']}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n🎉 Тестирование API завершено!")
    print("\n📋 Документация API доступна по адресу:")
    print("   http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    test_api()
