#!/usr/bin/env python3
"""
Детальный тест API с подробным выводом
"""

import requests
import json
import time

def test_detailed():
    """Детальный тест API"""
    print("🔍 ДЕТАЛЬНЫЙ ТЕСТ API")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    # Тест 1: Health check
    print("\n1. Проверка здоровья...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Сервис работает: {data['status']}")
            print(f"   Модель: {data['model']}")
        else:
            print(f"   ❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
    
    # Тест 2: Генерация тем с подробным выводом
    print("\n2. Генерация тем...")
    
    payload = {
        "field": "Информатика",
        "level": "Бакалавриат",
        "count": 2,
        "difficulty": "Средняя",
        "keywords": ["машинное обучение", "алгоритмы"]
    }
    
    print(f"   Отправляем запрос: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/generate-topics",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()
        
        print(f"   Статус: {response.status_code}")
        print(f"   Время: {end_time - start_time:.2f}с")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Успешно!")
            print(f"   Количество тем: {len(data.get('topics', []))}")
            
            for i, topic in enumerate(data.get('topics', []), 1):
                print(f"\n   Тема {i}:")
                print(f"     Заголовок: {topic.get('title', 'Нет заголовка')}")
                print(f"     Описание: {topic.get('description', 'Нет описания')}")
                print(f"     Ключевые слова: {topic.get('keywords', [])}")
                print(f"     Сложность: {topic.get('difficulty', 'Не указана')}")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
    
    # Тест 3: Простая генерация
    print("\n3. Простая генерация...")
    
    simple_payload = {
        "field": "Математика",
        "level": "Бакалавриат",
        "count": 1
    }
    
    try:
        response = requests.post(
            f"{base_url}/generate-topics",
            json=simple_payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Успешно! Тем: {len(data.get('topics', []))}")
            if data.get('topics'):
                topic = data['topics'][0]
                print(f"   Тема: {topic.get('title', 'Нет заголовка')}")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Исключение: {e}")

if __name__ == "__main__":
    test_detailed()
