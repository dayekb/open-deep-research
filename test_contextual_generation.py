#!/usr/bin/env python3
"""
Тест контекстной генерации тем ВКР
"""

import requests
import json
import time

def test_contextual_generation():
    """Тест генерации с контекстом"""
    print("🎯 ТЕСТ КОНТЕКСТНОЙ ГЕНЕРАЦИИ ТЕМ ВКР")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Тест 1: Генерация с предпочтениями студента
    print("\n1. Генерация с предпочтениями студента...")
    
    student_preferences = {
        "interests": ["машинное обучение", "компьютерное зрение", "нейронные сети"],
        "skills": ["Python", "TensorFlow", "OpenCV", "SQL"],
        "career_goals": ["Data Scientist", "ML Engineer"],
        "preferred_technologies": ["Python", "TensorFlow", "PyTorch", "Docker"],
        "work_style": "практический",
        "complexity_preference": "средняя"
    }
    
    payload = {
        "field": "Информатика",
        "level": "Бакалавриат",
        "count": 2,
        "student_preferences": student_preferences
    }
    
    try:
        response = requests.post(
            f"{base_url}/generate-topics",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Сгенерировано {len(data['topics'])} тем")
            
            for i, topic in enumerate(data['topics'], 1):
                print(f"\n   Тема {i}: {topic['title']}")
                print(f"   Ключевые слова: {topic['keywords']}")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
    
    # Тест 2: Генерация с контекстом кафедры
    print("\n2. Генерация с контекстом кафедры...")
    
    department_context = {
        "existing_topics": [
            "Разработка системы распознавания лиц",
            "Анализ данных социальных сетей",
            "Оптимизация алгоритмов сортировки"
        ],
        "research_directions": [
            "Искусственный интеллект",
            "Большие данные",
            "Кибербезопасность"
        ],
        "available_resources": [
            "GPU кластер",
            "База данных публикаций",
            "Лаборатория машинного обучения"
        ],
        "supervisor_expertise": [
            "Компьютерное зрение",
            "Обработка естественного языка",
            "Рекомендательные системы"
        ]
    }
    
    payload = {
        "field": "Информатика",
        "level": "Магистратура",
        "count": 2,
        "department_context": department_context,
        "avoid_duplicates": True
    }
    
    try:
        response = requests.post(
            f"{base_url}/generate-topics",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Сгенерировано {len(data['topics'])} тем")
            
            for i, topic in enumerate(data['topics'], 1):
                print(f"\n   Тема {i}: {topic['title']}")
                print(f"   Описание: {topic['description'][:100]}...")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
    
    # Тест 3: Полная персонализация
    print("\n3. Полная персонализация...")
    
    full_payload = {
        "field": "Информатика",
        "level": "Бакалавриат",
        "count": 1,
        "student_preferences": {
            "interests": ["веб-разработка", "мобильные приложения"],
            "skills": ["JavaScript", "React", "Node.js"],
            "career_goals": ["Frontend Developer"],
            "preferred_technologies": ["React", "Vue.js", "TypeScript"],
            "work_style": "практический",
            "complexity_preference": "легкая"
        },
        "department_context": {
            "existing_topics": [
                "Разработка веб-приложения для интернет-магазина",
                "Мобильное приложение для доставки еды"
            ],
            "research_directions": ["Веб-технологии", "UX/UI дизайн"],
            "available_resources": ["Сервер разработки", "Дизайн-студия"]
        },
        "avoid_duplicates": True
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/generate-topics",
            json=full_payload,
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Сгенерировано {len(data['topics'])} тем за {end_time - start_time:.2f}с")
            
            for i, topic in enumerate(data['topics'], 1):
                print(f"\n   Тема {i}: {topic['title']}")
                print(f"   Описание: {topic['description']}")
                print(f"   Ключевые слова: {topic['keywords']}")
                print(f"   Сложность: {topic.get('difficulty_level', 'Не указана')}")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Исключение: {e}")


if __name__ == "__main__":
    test_contextual_generation()
